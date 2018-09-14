-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.REQUEST_PARTY_VW;

create or replace view request_party_vw as
select  rp.request_id,
    rp.last_name,
    rp.first_name,
    rp.middle_name,
    rp.phone_number,
    rp.fax_number,
    rp.email_address,
    rp.contact,
    rp.client_first_name,
    rp.client_last_name,
    rp.decline_notification_ind,
    addr.addr_line_1,
    addr.addr_line_2,
    addr.addr_line_3,
    addr.city,
    addr.postal_cd,
    addr.state_province_cd,
    addr.country_type_cd
from request_party rp
left outer join address@global_readonly addr ON addr.addr_id = rp.address_id
left outer join request r on r.request_id = rp.request_id
where rp.party_type_cd = 'APP';


DROP PUBLIC SYNONYM REQUEST_PARTY_VW;

CREATE PUBLIC SYNONYM REQUEST_PARTY_VW FOR NAMEX.REQUEST_PARTY_VW;
