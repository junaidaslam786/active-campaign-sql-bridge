from .db import SessionLocal
from .models import MainInfoTable, ContactInfoTable
from datetime import date
import logging

AC_TO_DB_MAP = {
    "email": ("email_text", 180),
    "phone": ("phone_text", 120),
    "firstName": ("first_name_text", 40),
    "lastName": ("last_name_text", 40)
}

def safe_truncate(val, max_length):
    return val[:max_length] if isinstance(val, str) and max_length else val

def is_valid_email(email):
    # Very basic validation. For robust: use email-validator package.
    return email and "@" in email and "." in email

def sync_contacts_from_activecampaign(ac_contacts):
    db = SessionLocal()
    imported = 0
    updated = 0
    skipped_no_email = 0
    skipped_invalid_email = 0
    skipped_field_too_long = 0
    try:
        for ac_contact in ac_contacts:
            email = ac_contact.get("email", "").strip()
            if not email:
                skipped_no_email += 1
                # Log skip: missing email
                db.add(ContactInfoTable(
                    contact_date=date.today(),
                    link_to_maininfotableid=0,
                    notes="Skipped: missing email.",
                    type="skip"
                ))
                db.commit()
                continue
            if not is_valid_email(email):
                skipped_invalid_email += 1
                db.add(ContactInfoTable(
                    contact_date=date.today(),
                    link_to_maininfotableid=0,
                    notes=f"Skipped: invalid email: {email}",
                    type="skip"
                ))
                db.commit()
                continue

            contact_data = {}
            field_too_long = False
            for ac_field, (db_field, max_length) in AC_TO_DB_MAP.items():
                value = ac_contact.get(ac_field, None)
                if value is not None:
                    value = str(value).strip()
                    if len(value) > max_length:
                        field_too_long = True
                        db.add(ContactInfoTable(
                            contact_date=date.today(),
                            link_to_maininfotableid=0,
                            notes=f"Skipped: field '{db_field}' too long (>{max_length} chars) for email: {email}",
                            type="skip"
                        ))
                        db.commit()
                        break  # Don't import this contact
                    value = safe_truncate(value, max_length)
                    if value != "":
                        contact_data[db_field] = value
            if field_too_long:
                skipped_field_too_long += 1
                continue

            db_contact = db.query(MainInfoTable).filter(MainInfoTable.email_text == email).first()
            if db_contact:
                changes = []
                for field, new_value in contact_data.items():
                    old_value = getattr(db_contact, field)
                    if new_value != old_value and new_value != "" and new_value is not None:
                        changes.append(f"{field}: '{old_value}' → '{new_value}'")
                        setattr(db_contact, field, new_value)
                db_contact.groupcode_numtext = db_contact.groupcode_numtext or None
                if changes:
                    db.add(ContactInfoTable(
                        contact_date=date.today(),
                        link_to_maininfotableid=db_contact.maininfotableID,
                        notes="; ".join(changes),
                        type="update"
                    ))
                    db.commit()
                    updated += 1
            else:
                new_contact = MainInfoTable(
                    groupcode_numtext="99",
                    **contact_data
                )
                db.add(new_contact)
                db.commit()
                db.refresh(new_contact)
                db.add(ContactInfoTable(
                    contact_date=date.today(),
                    link_to_maininfotableid=new_contact.maininfotableID,
                    notes="Imported from ActiveCampaign",
                    type="add"
                ))
                db.commit()
                imported += 1

    except Exception as e:
        db.rollback()
        logging.error(f"Sync error: {e}")
        db.add(ContactInfoTable(
            contact_date=date.today(),
            link_to_maininfotableid=0,
            notes=f"Sync error: {str(e)}",
            type="error"
        ))
        db.commit()
    finally:
        db.close()
        print(f"Imported: {imported}, Updated: {updated}, Skipped (no email): {skipped_no_email}, Skipped (invalid email): {skipped_invalid_email}, Skipped (field too long): {skipped_field_too_long}")
