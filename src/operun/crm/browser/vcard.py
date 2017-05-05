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
    card.n.value = vobject.vcard.Name(family=obj.lastname, given=obj.firstname)
    # Fullname
    card.add('fn')
    card.fn.value = obj.title
    # E-Mail
    card.add('email')
    card.email.value = obj.email
    # Company
    card.add('org')
    card.org.value = [obj.account.to_object.Title()]
    # Account-Type
    card.add('title')
    card.title.value = obj.type.title()
    # UID
    card.add('uid')
    card.uid.value = obj.UID()
    # Phone
    card.add('tel')
    card.tel.value = obj.phone
    # Serialize
    return card.serialize()
