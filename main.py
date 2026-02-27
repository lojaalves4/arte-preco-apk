# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore

from core.pricing import calcular_preco
from core.license_core import validar_chave

STORE = JsonStore("artepreco_store.json")


def parse_float_br(s: str) -> float:
    """
    Aceita:
      - 10
      - 10.5
      - 10,5
      - 1.234,56
    """
    if s is None:
        return 0.0
    t = str(s).strip()
    if not t:
        return 0.0
    t = t.replace(" ", "")
    # remove separador de milhar e padroniza decimal
    t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except Exception:
        return 0.0


def parse_int(s: str, default: int = 0) -> int:
    try:
        # suporta "7", "7,0", "7.0"
        return int(float(str(s).replace(",", ".").strip()))
    except Exception:
        return default


def get_device_id():
    # Android ID (melhor no Android)
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        SettingsSecure = autoclass("android.provider.Settings$Secure")
        cr = PythonActivity.mActivity.getContentResolver()
        android_id = SettingsSecure.getString(cr, SettingsSecure.ANDROID_ID)
        if android_id:
            return str(android_id)
    except Exception:
        pass

    # fallback: id salvo localmente
    if STORE.exists("device"):
        return STORE.get("device").get("id", "")

    import uuid
    did = str(uuid.uuid4())
    STORE.put("device", id=did)
    return did


class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=12, spacing=10, **kwargs)

        self.device_id = get_device_id()

        self.add_widget(Label(text="Arte Preço Pro (Offline)", font_size=22, size_hint_y=None, height=40))

        self.status = Label(text="", size_hint_y=None, height=26)
        self.add_widget(self.status)

        self.body = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.body.bind(minimum_height=self.body.setter("height"))

        sv = ScrollView()
        sv.add_widget(self.body)
        self.add_widget(sv)

        self._render()

    def is_activated(self):
        return STORE.exists("license") and STORE.get("license").get("ok", False) is True

    def _render(self):
        self.body.clear_widgets()
        if not self.is_activated():
            self._render_activation()
        else:
            self._render_calc()

    def _render_activation(self):
        self.status.text = "Ative para usar. Envie o ID do aparelho para gerar a chave."

        self.body.add_widget(Label(text="ID do Aparelho (copie e envie):", size_hint_y=None, height=26))
        did = TextInput(text=self.device_id, readonly=True, multiline=False, size_hint_y=None, height=44)
        self.body.add_widget(did)

        self.body.add_widget(Label(text="Cole a chave (APO-...):", size_hint_y=None, height=26))
        self.key_input = TextInput(text="", multiline=False, size_hint_y=None, height=44)
        self.body.add_widget(self.key_input)

        b = Button(text="Ativar", size_hint_y=None, height=48)
        b.bind(on_press=self._activate)
        self.body.add_widget(b)

    def _activate(self, _btn):
        key = (self.key_input.text or "").strip()
        ok, msg = validar_chave(key, self.device_id)
        if ok:
            STORE.put("license", ok=True, key=key, msg=msg)
            self._popup("Sucesso", msg)
            self._render()
        else:
            self._popup("Erro", msg)

    def _render_calc(self):
        self.status.text = STORE.get("license").get("msg", "Ativado")

        def field(label, hint=""):
            self.body.add_widget(Label(text=label, size_hint_y=None, height=26))
            ti = TextInput(text="", hint_text=hint, multiline=False, size_hint_y=None, height=44)
            self.body.add_widget(ti)
            return ti

        self.produto = field("Produto")
        self.material = field("Material (R$)", "ex: 25,50")
        self.horas = field("Horas", "ex: 2")
        self.valor_hora = field("Valor hora (R$)", "ex: 30")
        self.despesas = field("Despesas (R$)", "ex: 10")
        self.margem = field("Margem (%)", "ex: 30")
        self.validade = field("Validade (dias)", "ex: 7")
        self.validade.text = "7"

        b = Button(text="Calcular", size_hint_y=None, height=52)
        b.bind(on_press=self._calc)
        self.body.add_widget(b)

        self.res = Label(text="", size_hint_y=None, height=140)
        self.body.add_widget(self.res)

        sair = Button(text="Desativar neste aparelho", size_hint_y=None, height=48)
        sair.bind(on_press=self._logout)
        self.body.add_widget(sair)

    def _calc(self, _btn):
        try:
            r = calcular_preco(
                produto=(self.produto.text or "").strip(),
                material=parse_float_br(self.material.text),
                horas=parse_float_br(self.horas.text),
                valor_hora=parse_float_br(self.valor_hora.text),
                despesas=parse_float_br(self.despesas.text),
                margem=parse_float_br(self.margem.text),
                validade_dias=parse_int(self.validade.text, default=7),
            )

            self.res.text = (
                f"Preço final: R$ {r['preco_final']:.2f}\n"
                f"Custo total: R$ {r['custo_total']:.2f}\n"
                f"Emissão: {r['data_emissao']}\n"
                f"Validade: {r['data_validade']}"
            )
        except Exception:
            self._popup("Erro", "Verifique os valores digitados.")

    def _logout(self, _btn):
        if STORE.exists("license"):
            STORE.delete("license")
        self._popup("Ok", "Desativado neste aparelho.")
        self._render()

    def _popup(self, title, msg):
        box = BoxLayout(orientation="vertical", padding=12, spacing=10)
        box.add_widget(Label(text=msg))
        bt = Button(text="OK", size_hint_y=None, height=44)
        box.add_widget(bt)
        p = Popup(title=title, content=box, size_hint=(0.9, 0.5))
        bt.bind(on_press=p.dismiss)
        p.open()


class ArtePrecoOfflineApp(App):
    def build(self):
        return Root()


if __name__ == "__main__":
    ArtePrecoOfflineApp().run()