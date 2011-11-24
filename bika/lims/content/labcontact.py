"""The lab staff

$Id: LabContact.py 639 2007-03-20 09:35:32Z anneline $
"""
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import manage_users
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *
from Products.Archetypes.references import HoldingReference
from bika.lims.content.person import Person
from bika.lims.config import ManageClients, PUBLICATION_PREFS, PROJECTNAME, \
    I18N_DOMAIN
from bika.lims import bikaMessageFactory as _
import sys

schema = Person.schema.copy() + Schema((
    ImageField('Signature',
        widget = ImageWidget(
            label = _("Signature"),
            description = _("Upload a scanned signature to be used on printed analysis "
                            "results reports. Ideal size is 250 pixels wide by 150 high"),
        ),
    ),
    ReferenceField('Department',
        required = 0,
        vocabulary_display_path_bound = sys.maxint,
        allowed_types = ('Department',),
        relationship = 'LabContactDepartment',
        vocabulary = 'getDepartments',
        referenceClass = HoldingReference,
        widget = ReferenceWidget(
            checkbox_bound = 1,
            label = _("Department"),
            description = _("The laboratory department in which this contact works"),
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    ComputedField('DepartmentTitle',
        expression = "context.getDepartment() and context.getDepartment().Title() or ''",
        widget = ComputedWidget(
            visible = False,
        ),
    ),
))

schema['JobTitle'].schemata = 'default'
# Don't make title required - it will be computed from the Person's Fullname
schema['title'].required = 0
schema['title'].widget.visible = False

class LabContact(Person):
    security = ClassSecurityInfo()
    schema = schema

    def Title(self):
        """ Return the contact's Fullname as title """
        return self.getFullname()

    def getDepartments(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [('','')] + [(o.UID, o.Title) for o in \
                               bsc(portal_type='Department',
                                   inactive_state = 'active')]
        o = self.getDepartment()
        if o and (o.UID(), o.Title()) not in items:
            items.append((o.UID(), o.Title()))
        items.sort(lambda x,y: cmp(x[1], y[1]))
        return DisplayList(list(items))

registerType(LabContact, PROJECTNAME)
