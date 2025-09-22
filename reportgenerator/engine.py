import html
import enum
from typing import Optional, List
from pydantic import BaseModel
try:
    from .htmlrenderer import HTMLRenderer
except ImportError:
    from htmlrenderer import HTMLRenderer

class Engine:
    def __init__(self, renderer=None):
        self.parts = []
        self.renderer = renderer or HTMLRenderer()

    def write(self, text: str):
        self.parts.append(text)

    def write_header(self, title: str, level: int):
        self.parts.append(self.renderer.render_header(title, level))

    def write_input(self, model: BaseModel, title: Optional[str] = None, fields: Optional[list[str]] = None):
        if title:
            self.write_header(title, 4)
        self.parts.append('<form method="post">')
        model_fields = type(model).model_fields
        field_names = fields if fields is not None else list(model_fields.keys())
        rows = []
        for name in field_names:
            field = model_fields[name]
            label = field.title or name
            value = getattr(model, name)
            annotation = field.annotation
            if isinstance(annotation, type) and issubclass(annotation, enum.Enum):
                input_html = self.renderer.render_input_enum(name, value, annotation)
            elif annotation is bool:
                input_html = self.renderer.render_input_checkbox(name, value)
            elif annotation in (int, float):
                input_html = self.renderer.render_input_number(name, value)
            else:
                input_html = self.renderer.render_input_text(name, value)
            rows.append(self.renderer.render_row(name, label, input_html))
        self.parts.append(self.renderer.render_table(rows))
        self.parts.append('<input type="submit" value="Beregn"></form>')

    def write_model(self, model: BaseModel, fields: Optional[list[str]] = None, table_style: Optional[str] = None):
        model_fields = type(model).model_fields
        field_names = fields if fields is not None else list(model_fields.keys())
        rows = []
        for name in field_names:
            field = model_fields[name]
            label = field.title or name
            value = getattr(model, name)
            rows.append(self.renderer.render_row(name, label, html.escape(str(value))))
        self.parts.append(self.renderer.render_table(rows, table_style=table_style))

    def write_model_table(self, models: list[BaseModel], headers: list[str], fields: Optional[list[str]] = None, title: Optional[str] = None):
        if title:
            self.write_header(title, 4)
        self.parts.append(self.renderer.render_model_table(models, headers, fields, title=None))

    def get_html(self) -> str:
        return "\n".join(self.parts)

