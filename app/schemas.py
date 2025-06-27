from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# ---------- MAININFOTABLE SCHEMAS ----------

class MainInfoBase(BaseModel):
    academic_program_dd: Optional[str] = None
    accepted_date: Optional[date] = None
    act_sat_dd: Optional[str] = None
    address1_text: Optional[str] = None
    address2_text: Optional[str] = None
    admin_flag_cb: Optional[int] = None
    admis_status_dd: Optional[str] = None
    affidavit_of_support_cb: Optional[int] = None
    alumni_text: Optional[str] = None
    alumni_cb: Optional[int] = None
    application_date: Optional[date] = None
    best_time_to_call_text: Optional[str] = None
    church_referral_cb: Optional[int] = None
    city_text: Optional[str] = None
    date_entered: Optional[date] = None
    date_of_birth_date: Optional[date] = None
    denomination: Optional[str] = None
    deposit_cb: Optional[int] = None
    distance: Optional[str] = None
    doctrine_cb: Optional[int] = None
    email_text: Optional[EmailStr] = None
    email_request_cb: Optional[int] = None
    explain_info_text: Optional[str] = None
    application_fee_dd: Optional[str] = None
    feel_a_call_text: Optional[str] = None
    finaid_rpt_sent_date: Optional[date] = None
    first_name_text: Optional[str] = None
    folder_location: Optional[int] = None
    funnel_location: Optional[str] = None
    grad_date_numtext: Optional[int] = 0
    health_form_cb: Optional[int] = None
    hs_transcript_cb: Optional[int] = None
    facebook_text: Optional[str] = None
    international_student_cb: Optional[int] = None
    isr_date: Optional[date] = None
    isr_is_valid_cb: Optional[int] = None
    kmbc_groups_dd: Optional[str] = None
    lack_of_program_cb: Optional[int] = None
    last_call_date: Optional[date] = None
    last_contact_date: Optional[date] = None
    last_email_date: Optional[date] = None
    last_im_date: Optional[date] = None
    last_letter_date: Optional[date] = None
    last_name_text: Optional[str] = None
    last_personal_visit_date: Optional[date] = None
    last_updated: Optional[date] = None
    letter_sent_date: Optional[date] = None
    marital_status_dd: Optional[str] = None
    medical_release_cb: Optional[int] = None
    money_cb: Optional[str] = None
    no_auto_email_cb: Optional[int] = None
    non_traditional_cb: Optional[int] = None
    number_of_visits_dd: Optional[str] = None
    other_contact: Optional[str] = None
    other_admin_text: Optional[str] = None
    other_obstacle_cb: Optional[int] = None
    pastor_church_text: Optional[str] = None
    pastor_church_cb: Optional[int] = None
    phone_text: Optional[str] = None
    picture_cb: Optional[int] = None
    post_hs_transcript_cb: Optional[int] = None
    prospect_type: Optional[str] = None
    provisional_acceptance_cb: Optional[int] = None
    queue_action_dd: Optional[str] = None
    rec_date_of_review_date: Optional[date] = None
    recommendations_dd: Optional[int] = None
    rules_cb: Optional[int] = None
    sch_app_rcvd_cb: Optional[int] = None
    applied_semester_dd: Optional[str] = None
    sex_dd: Optional[str] = None
    special_interest_cb: Optional[int] = None
    ss_number_text: Optional[str] = None
    state: Optional[str] = None
    testimony_cb: Optional[int] = None
    toefl_dd: Optional[str] = None
    final_transcript_cb: Optional[int] = None
    visit_1: Optional[int] = None
    visit_2: Optional[int] = None
    visit_3: Optional[int] = None
    visited_campus_date: Optional[date] = None
    website_cb: Optional[int] = None
    work_app: Optional[int] = None
    applied_year_text: Optional[int] = None
    zipcode: Optional[str] = None
    groupcode_numtext: Optional[str] = None
    instructions_text: Optional[str] = None
    school_text: Optional[str] = None
    downpayment_cb: Optional[int] = None
    populi_id: Optional[int] = None
    txt_optin_cb: Optional[int] = 0
    primary_email_text: Optional[EmailStr] = None

class MainInfoCreate(MainInfoBase):
    pass

class MainInfoUpdate(MainInfoBase):
    pass

class MainInfoResponse(MainInfoBase):
    maininfotableID: int

    class Config:
        orm_mode = True

# ---------- CONTACTINFOTABLE SCHEMAS ----------

class ContactInfoBase(BaseModel):
    contact_date: Optional[date] = None
    link_to_maininfotableid: int = Field(..., description="FK to maininfotable.maininfotableID")
    notes: Optional[str] = None
    person: Optional[str] = None
    type: Optional[str] = None
    contact_time: Optional[str] = None

class ContactInfoCreate(ContactInfoBase):
    pass

class ContactInfoResponse(ContactInfoBase):
    contactinfotableid: int

    class Config:
        from_attributes = True


# For MainInfoTable operations
ContactCreate = MainInfoCreate
ContactUpdate = MainInfoUpdate
ContactResponse = MainInfoResponse

# For ContactInfoTable operations
NoteCreate = ContactInfoCreate
NoteResponse = ContactInfoResponse