import frappe
from frappe import _
from frappe.custom.doctype.customize_form.customize_form import (
    CustomizeForm as _CustomizeForm,
)

from india_compliance.audit_trail.utils import (
    get_audit_trail_doctypes,
    is_audit_trail_enabled,
)


class CustomizeForm(_CustomizeForm):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.core.doctype.doctype_action.doctype_action import DocTypeAction
        from frappe.core.doctype.doctype_link.doctype_link import DocTypeLink
        from frappe.core.doctype.doctype_state.doctype_state import DocTypeState
        from frappe.custom.doctype.customize_form_field.customize_form_field import CustomizeFormField
        from frappe.types import DF

        actions: DF.Table[DocTypeAction]
        allow_auto_repeat: DF.Check
        allow_copy: DF.Check
        allow_import: DF.Check
        autoname: DF.Data | None
        default_email_template: DF.Link | None
        default_print_format: DF.Link | None
        default_view: DF.Literal[None]
        doc_type: DF.Link | None
        editable_grid: DF.Check
        email_append_to: DF.Check
        fields: DF.Table[CustomizeFormField]
        force_re_route_to_default_view: DF.Check
        image_field: DF.Data | None
        is_calendar_and_gantt: DF.Check
        istable: DF.Check
        label: DF.Data | None
        link_filters: DF.JSON | None
        links: DF.Table[DocTypeLink]
        make_attachments_public: DF.Check
        max_attachments: DF.Int
        naming_rule: DF.Literal["", "Set by user", "By fieldname", "By \"Naming Series\" field", "Expression", "Expression (old style)", "Random", "By script"]
        queue_in_background: DF.Check
        quick_entry: DF.Check
        search_fields: DF.Data | None
        sender_field: DF.Data | None
        sender_name_field: DF.Data | None
        show_preview_popup: DF.Check
        show_title_field_in_link: DF.Check
        sort_field: DF.Literal[None]
        sort_order: DF.Literal["ASC", "DESC"]
        states: DF.Table[DocTypeState]
        subject_field: DF.Data | None
        title_field: DF.Data | None
        track_changes: DF.Check
        track_views: DF.Check
        translated_doctype: DF.Check
    # end: auto-generated types
    @frappe.whitelist()
    def fetch_to_customize(self):
        self.set_onload(
            "audit_trail_enabled",
            self.doc_type
            and is_audit_trail_enabled()
            and self.doc_type in get_audit_trail_doctypes(),
        )

        return super().fetch_to_customize()

    @frappe.whitelist()
    def save_customization(self):
        self.validate_audit_trail_integrity()
        return super().save_customization()

    def validate_audit_trail_integrity(self):
        if (
            not self.doc_type
            or self.track_changes
            or not is_audit_trail_enabled()
            or self.doc_type not in get_audit_trail_doctypes()
        ):
            return

        frappe.throw(
            _(
                "Cannot disable Track Changes for {0}, since it has been enabled to"
                " maintain Audit Trail"
            ).format(_(self.doc_type))
        )
