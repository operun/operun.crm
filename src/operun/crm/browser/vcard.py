# -*- coding: utf-8 -*-

import vobject


def generate_vcard(obj):
    """
    Generates a vCard from the object attributes.
    """
    # vCard
    card = vobject.vCard()
    # Name
    card.add('n')
    card.n.value = vobject.vcard.Name(
        family=(obj.lastname or ''),
        given=(obj.firstname or ''),
    )
    # Fullname
    card.add('fn')
    card.fn.value = (obj.title or '')
    # E-Mail
    card.add('email')
    card.email.value = (obj.email or '')
    # Company
    card.add('org')
    account = (obj.account or '')
    if account:
        account = account.to_object.Title()
    card.org.value = [account]
    # Account-Type
    card.add('title')
    card.title.value = (obj.type.title() or '')
    # UID
    card.add('uid')
    card.uid.value = (obj.UID() or '')
    # Phone
    card.add('tel')
    card.tel.value = (obj.phone or '')
    # Serialize
    return card.serialize()
