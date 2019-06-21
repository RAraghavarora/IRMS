# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountOffsetTypes(models.Model):
    type = models.CharField(primary_key=True, max_length=16)

    class Meta:
        managed = False
        db_table = 'account_offset_types'


class AccountOffsets(models.Model):
    # id is the primary key
    credit = models.ForeignKey('Accountlines', related_name='offsets_credited', on_delete=models.SET_NULL, blank=True, null=True) # The accountline that increased the patron's balance
    debit = models.ForeignKey('Accountlines', related_name='offsets_debited', on_delete=models.SET_NULL, blank=True, null=True) # The accountline that decreased the patron's balance
    type = models.ForeignKey(AccountOffsetTypes, on_delete=models.CASCADE, db_column='type')
    amount = models.DecimalField(max_digits=26, decimal_places=6)
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'account_offsets'


class Accountlines(models.Model):
    accountlines_id = models.AutoField(primary_key=True)
    issue_id = models.IntegerField(blank=True, null=True)
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    accountno = models.SmallIntegerField()
    itemnumber = models.ForeignKey('Items', models.DO_NOTHING, db_column='itemnumber', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True) # Amount of the fine/invoice
    description = models.TextField(blank=True, null=True)
    accounttype = models.CharField(max_length=5, blank=True, null=True)
    payment_type = models.CharField(max_length=80, blank=True, null=True)
    amountoutstanding = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True) # Remaining amount after receiving / sending the payment
    lastincrement = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    timestamp = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accountlines'


class ActionLogs(models.Model):
    action_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    user = models.IntegerField()
    module = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    object = models.IntegerField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    interface = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_logs'


class AdditionalFieldValues(models.Model):
    # id is the primary key
    field = models.ForeignKey('AdditionalFields', models.DO_NOTHING)
    record_id = models.IntegerField()
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'additional_field_values'
        unique_together = (('field', 'record_id'),)


class AdditionalFields(models.Model):
    tablename = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    authorised_value_category = models.CharField(max_length=16)
    marcfield = models.CharField(max_length=16)
    searchable = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'additional_fields'
        unique_together = (('tablename', 'name'),)


class Alert(models.Model):
    alertid = models.AutoField(primary_key=True)
    borrowernumber = models.IntegerField()
    type = models.CharField(max_length=10)
    externalid = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'alert'


class ApiKeys(models.Model):
    client_id = models.CharField(primary_key=True, max_length=191)
    secret = models.CharField(unique=True, max_length=191)
    description = models.CharField(max_length=255)
    patron = models.ForeignKey('Borrowers', models.DO_NOTHING)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'api_keys'


class Aqbasket(models.Model):
    basketno = models.AutoField(primary_key=True)
    basketname = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    booksellernote = models.TextField(blank=True, null=True)
    contractnumber = models.ForeignKey('Aqcontract', models.DO_NOTHING, db_column='contractnumber', blank=True, null=True)
    creationdate = models.DateField(blank=True, null=True)
    closedate = models.DateField(blank=True, null=True)
    booksellerid = models.ForeignKey('Aqbooksellers', models.DO_NOTHING, db_column='booksellerid')
    authorisedby = models.CharField(max_length=10, blank=True, null=True)
    booksellerinvoicenumber = models.TextField(blank=True, null=True)
    basketgroupid = models.ForeignKey('Aqbasketgroups', models.DO_NOTHING, db_column='basketgroupid', blank=True, null=True)
    deliveryplace = models.CharField(max_length=10, blank=True, null=True)
    billingplace = models.CharField(max_length=10, blank=True, null=True)
    branch = models.ForeignKey('Branches', models.DO_NOTHING, db_column='branch', blank=True, null=True)
    is_standing = models.IntegerField()
    create_items = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqbasket'


class Aqbasketgroups(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    closed = models.IntegerField(blank=True, null=True)
    booksellerid = models.ForeignKey('Aqbooksellers', models.DO_NOTHING, db_column='booksellerid')
    deliveryplace = models.CharField(max_length=10, blank=True, null=True)
    freedeliveryplace = models.TextField(blank=True, null=True)
    deliverycomment = models.CharField(max_length=255, blank=True, null=True)
    billingplace = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqbasketgroups'


class Aqbasketusers(models.Model):
    basketno = models.OneToOneField(Aqbasket, models.DO_NOTHING, db_column='basketno', primary_key=True)
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber')

    class Meta:
        managed = False
        db_table = 'aqbasketusers'
        unique_together = (('basketno', 'borrowernumber'),)


class Aqbooksellers(models.Model):
    name = models.TextField() # Vendor name
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    address3 = models.TextField(blank=True, null=True)
    address4 = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    accountnumber = models.TextField(blank=True, null=True)
    othersupplier = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10)
    booksellerfax = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    bookselleremail = models.TextField(blank=True, null=True)
    booksellerurl = models.TextField(blank=True, null=True)
    postal = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    listprice = models.ForeignKey('Currency', related_name='aqsellers_listed', on_delete=models.SET_NULL, db_column='listprice', blank=True, null=True)
    invoiceprice = models.ForeignKey('Currency', related_name='aqsellers_invoiced', on_delete=models.SET_NULL, db_column='invoiceprice', blank=True, null=True)
    gstreg = models.IntegerField(blank=True, null=True)
    listincgst = models.IntegerField(blank=True, null=True)
    invoiceincgst = models.IntegerField(blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    deliverytime = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqbooksellers'


class Aqbudgetborrowers(models.Model):
    budget = models.OneToOneField('Aqbudgets', models.DO_NOTHING, primary_key=True)
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber')

    class Meta:
        managed = False
        db_table = 'aqbudgetborrowers'
        unique_together = (('budget', 'borrowernumber'),)


class Aqbudgetperiods(models.Model):
    budget_period_id = models.AutoField(primary_key=True)
    budget_period_startdate = models.DateField()
    budget_period_enddate = models.DateField()
    budget_period_active = models.IntegerField(blank=True, null=True)
    budget_period_description = models.TextField(blank=True, null=True)
    budget_period_total = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    budget_period_locked = models.IntegerField(blank=True, null=True)
    sort1_authcat = models.CharField(max_length=10, blank=True, null=True)
    sort2_authcat = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqbudgetperiods'


class Aqbudgets(models.Model):
    budget_id = models.AutoField(primary_key=True)
    budget_parent_id = models.IntegerField(blank=True, null=True)
    budget_code = models.CharField(max_length=30, blank=True, null=True)
    budget_name = models.CharField(max_length=80, blank=True, null=True)
    budget_branchcode = models.CharField(max_length=10, blank=True, null=True)
    budget_amount = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    budget_encumb = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    budget_expend = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    budget_notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    budget_period_id = models.IntegerField(blank=True, null=True)
    sort1_authcat = models.CharField(max_length=80, blank=True, null=True)
    sort2_authcat = models.CharField(max_length=80, blank=True, null=True)
    budget_owner_id = models.IntegerField(blank=True, null=True)
    budget_permission = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqbudgets'


class AqbudgetsPlanning(models.Model):
    plan_id = models.AutoField(primary_key=True)
    budget = models.ForeignKey(Aqbudgets, models.DO_NOTHING)
    budget_period_id = models.IntegerField()
    estimated_amount = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    authcat = models.CharField(max_length=30)
    authvalue = models.CharField(max_length=30)
    display = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqbudgets_planning'


class Aqcontacts(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    altphone = models.CharField(max_length=100, blank=True, null=True)
    fax = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    orderacquisition = models.IntegerField()
    claimacquisition = models.IntegerField()
    claimissues = models.IntegerField()
    acqprimary = models.IntegerField()
    serialsprimary = models.IntegerField()
    booksellerid = models.ForeignKey(Aqbooksellers, models.DO_NOTHING, db_column='booksellerid')

    class Meta:
        managed = False
        db_table = 'aqcontacts'


class Aqcontract(models.Model):
    contractnumber = models.AutoField(primary_key=True)
    contractstartdate = models.DateField(blank=True, null=True)
    contractenddate = models.DateField(blank=True, null=True)
    contractname = models.CharField(max_length=50, blank=True, null=True)
    contractdescription = models.TextField(blank=True, null=True)
    booksellerid = models.ForeignKey(Aqbooksellers, models.DO_NOTHING, db_column='booksellerid')

    class Meta:
        managed = False
        db_table = 'aqcontract'


class AqinvoiceAdjustments(models.Model):
    adjustment_id = models.AutoField(primary_key=True)
    invoiceid = models.ForeignKey('Aqinvoices', models.DO_NOTHING, db_column='invoiceid')
    adjustment = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    reason = models.CharField(max_length=80, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    budget = models.ForeignKey(Aqbudgets, models.DO_NOTHING, blank=True, null=True)
    encumber_open = models.SmallIntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aqinvoice_adjustments'


class Aqinvoices(models.Model):
    invoiceid = models.AutoField(primary_key=True)
    invoicenumber = models.TextField()
    booksellerid = models.ForeignKey(Aqbooksellers, models.DO_NOTHING, db_column='booksellerid')
    shipmentdate = models.DateField(blank=True, null=True)
    billingdate = models.DateField(blank=True, null=True)
    closedate = models.DateField(blank=True, null=True)
    shipmentcost = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    shipmentcost_budgetid = models.ForeignKey(Aqbudgets, models.DO_NOTHING, db_column='shipmentcost_budgetid', blank=True, null=True)
    message = models.ForeignKey('EdifactMessages', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqinvoices'


class AqorderUsers(models.Model):
    ordernumber = models.OneToOneField('Aqorders', models.DO_NOTHING, db_column='ordernumber', primary_key=True)
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber')

    class Meta:
        managed = False
        db_table = 'aqorder_users'
        unique_together = (('ordernumber', 'borrowernumber'),)


class Aqorders(models.Model):
    ordernumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey('Biblio', models.DO_NOTHING, db_column='biblionumber', blank=True, null=True)
    entrydate = models.DateField(blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    currency = models.ForeignKey('Currency', models.DO_NOTHING, db_column='currency', blank=True, null=True)
    listprice = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    datereceived = models.DateField(blank=True, null=True)
    invoiceid = models.ForeignKey(Aqinvoices, models.DO_NOTHING, db_column='invoiceid', blank=True, null=True)
    freight = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    unitprice = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    unitprice_tax_excluded = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    unitprice_tax_included = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    quantityreceived = models.SmallIntegerField()
    created_by = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    datecancellationprinted = models.DateField(blank=True, null=True)
    cancellationreason = models.TextField(blank=True, null=True)
    order_internalnote = models.TextField(blank=True, null=True)
    order_vendornote = models.TextField(blank=True, null=True)
    purchaseordernumber = models.TextField(blank=True, null=True)
    basketno = models.ForeignKey(Aqbasket, models.DO_NOTHING, db_column='basketno', blank=True, null=True)
    timestamp = models.DateTimeField()
    rrp = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    replacementprice = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    rrp_tax_excluded = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    rrp_tax_included = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    ecost = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    ecost_tax_excluded = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    ecost_tax_included = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    tax_rate_bak = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    tax_rate_on_ordering = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    tax_rate_on_receiving = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    tax_value_bak = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    tax_value_on_ordering = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    tax_value_on_receiving = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    budget = models.ForeignKey(Aqbudgets, models.DO_NOTHING)
    budgetdate = models.DateField(blank=True, null=True)
    sort1 = models.CharField(max_length=80, blank=True, null=True)
    sort2 = models.CharField(max_length=80, blank=True, null=True)
    sort1_authcat = models.CharField(max_length=10, blank=True, null=True)
    sort2_authcat = models.CharField(max_length=10, blank=True, null=True)
    uncertainprice = models.IntegerField(blank=True, null=True)
    claims_count = models.IntegerField(blank=True, null=True)
    claimed_date = models.DateField(blank=True, null=True)
    subscriptionid = models.ForeignKey('Subscription', models.DO_NOTHING, db_column='subscriptionid', blank=True, null=True)
    parent_ordernumber = models.IntegerField(blank=True, null=True)
    orderstatus = models.CharField(max_length=16, blank=True, null=True)
    line_item_id = models.CharField(max_length=35, blank=True, null=True)
    suppliers_reference_number = models.CharField(max_length=35, blank=True, null=True)
    suppliers_reference_qualifier = models.CharField(max_length=3, blank=True, null=True)
    suppliers_report = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqorders'


class AqordersItems(models.Model):
    ordernumber = models.ForeignKey(Aqorders, models.DO_NOTHING, db_column='ordernumber')
    itemnumber = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aqorders_items'


class AqordersTransfers(models.Model):
    ordernumber_from = models.OneToOneField(Aqorders, models.DO_NOTHING, related_name='transfers_given', db_column='ordernumber_from', unique=True, blank=True, null=True)
    ordernumber_to = models.OneToOneField(Aqorders, models.DO_NOTHING, related_name='transfers_received', db_column='ordernumber_to', unique=True, blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aqorders_transfers'


class ArticleRequests(models.Model):
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber')
    biblionumber = models.ForeignKey('Biblio', models.DO_NOTHING, db_column='biblionumber')
    itemnumber = models.ForeignKey('Items', models.DO_NOTHING, db_column='itemnumber', blank=True, null=True)
    branchcode = models.ForeignKey('Branches', models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    volume = models.TextField(blank=True, null=True)
    issue = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    pages = models.TextField(blank=True, null=True)
    chapters = models.TextField(blank=True, null=True)
    patron_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_requests'


class AudioAlerts(models.Model):
    precedence = models.PositiveSmallIntegerField()
    selector = models.CharField(max_length=255)
    sound = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'audio_alerts'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthHeader(models.Model):
    authid = models.BigAutoField(primary_key=True)
    authtypecode = models.CharField(max_length=10)
    datecreated = models.DateField(blank=True, null=True)
    modification_time = models.DateTimeField()
    origincode = models.CharField(max_length=20, blank=True, null=True)
    authtrees = models.TextField(blank=True, null=True)
    marc = models.TextField(blank=True, null=True)
    linkid = models.BigIntegerField(blank=True, null=True)
    marcxml = models.TextField()

    class Meta:
        managed = False
        db_table = 'auth_header'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthSubfieldStructure(models.Model):
    authtypecode = models.OneToOneField('AuthTypes', models.DO_NOTHING, db_column='authtypecode', primary_key=True)
    tagfield = models.CharField(max_length=3)
    tagsubfield = models.CharField(max_length=1)
    liblibrarian = models.CharField(max_length=255)
    libopac = models.CharField(max_length=255)
    repeatable = models.IntegerField()
    mandatory = models.IntegerField()
    tab = models.IntegerField(blank=True, null=True)
    authorised_value = models.CharField(max_length=10, blank=True, null=True)
    value_builder = models.CharField(max_length=80, blank=True, null=True)
    seealso = models.CharField(max_length=255, blank=True, null=True)
    isurl = models.IntegerField(blank=True, null=True)
    hidden = models.IntegerField()
    linkid = models.IntegerField()
    kohafield = models.CharField(max_length=45, blank=True, null=True)
    frameworkcode = models.CharField(max_length=10)
    defaultvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_subfield_structure'
        unique_together = (('authtypecode', 'tagfield', 'tagsubfield'),)


class AuthTagStructure(models.Model):
    authtypecode = models.OneToOneField('AuthTypes', models.DO_NOTHING, db_column='authtypecode', primary_key=True)
    tagfield = models.CharField(max_length=3)
    liblibrarian = models.CharField(max_length=255)
    libopac = models.CharField(max_length=255)
    repeatable = models.IntegerField()
    mandatory = models.IntegerField()
    authorised_value = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_tag_structure'
        unique_together = (('authtypecode', 'tagfield'),)


class AuthTypes(models.Model):
    authtypecode = models.CharField(primary_key=True, max_length=10)
    authtypetext = models.CharField(max_length=255)
    auth_tag_to_report = models.CharField(max_length=3)
    summary = models.TextField()

    class Meta:
        managed = False
        db_table = 'auth_types'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthorisedValueCategories(models.Model):
    category_name = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'authorised_value_categories'


class AuthorisedValues(models.Model):
    category = models.ForeignKey(AuthorisedValueCategories, models.DO_NOTHING, db_column='category')
    authorised_value = models.CharField(max_length=80)
    lib = models.CharField(max_length=200, blank=True, null=True)
    lib_opac = models.CharField(max_length=200, blank=True, null=True)
    imageurl = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authorised_values'


class AuthorisedValuesBranches(models.Model):
    av = models.ForeignKey(AuthorisedValues, models.DO_NOTHING)
    branchcode = models.ForeignKey('Branches', models.DO_NOTHING, db_column='branchcode')

    class Meta:
        managed = False
        db_table = 'authorised_values_branches'


class Biblio(models.Model):
    biblionumber = models.AutoField(primary_key=True)
    frameworkcode = models.CharField(max_length=4)
    author = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    unititle = models.TextField(blank=True, null=True) # uniform title (without the subtitle) from the MARC record
    notes = models.TextField(blank=True, null=True)
    serial = models.IntegerField(blank=True, null=True) # Boolean indicating whether biblio is for a serial
    seriestitle = models.TextField(blank=True, null=True)
    copyrightdate = models.SmallIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField() # date and time this record was last touched
    datecreated = models.DateField()
    abstract = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio'


class BiblioFramework(models.Model):
    frameworkcode = models.CharField(primary_key=True, max_length=4)
    frameworktext = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'biblio_framework'


class BiblioMetadata(models.Model):
    biblionumber = models.OneToOneField(Biblio, models.DO_NOTHING, db_column='biblionumber')
    format = models.CharField(max_length=16)
    marcflavour = models.CharField(max_length=16)
    metadata = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'biblio_metadata'
        unique_together = (('biblionumber', 'format', 'marcflavour'),)


class Biblioimages(models.Model):
    imagenumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    mimetype = models.CharField(max_length=15)
    imagefile = models.TextField()
    thumbnail = models.TextField()

    class Meta:
        managed = False
        db_table = 'biblioimages'


class Biblioitems(models.Model):
    biblioitemnumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    volume = models.TextField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)
    itemtype = models.CharField(max_length=10, blank=True, null=True)
    isbn = models.TextField(blank=True, null=True)
    issn = models.TextField(blank=True, null=True)
    ean = models.TextField(blank=True, null=True)
    publicationyear = models.TextField(blank=True, null=True)
    publishercode = models.CharField(max_length=255, blank=True, null=True)
    volumedate = models.DateField(blank=True, null=True)
    volumedesc = models.TextField(blank=True, null=True)
    collectiontitle = models.TextField(blank=True, null=True)
    collectionissn = models.TextField(blank=True, null=True)
    collectionvolume = models.TextField(blank=True, null=True)
    editionstatement = models.TextField(blank=True, null=True)
    editionresponsibility = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    illus = models.CharField(max_length=255, blank=True, null=True)
    pages = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    lccn = models.CharField(max_length=25, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    cn_source = models.CharField(max_length=10, blank=True, null=True)
    cn_class = models.CharField(max_length=30, blank=True, null=True)
    cn_item = models.CharField(max_length=10, blank=True, null=True)
    cn_suffix = models.CharField(max_length=10, blank=True, null=True)
    cn_sort = models.CharField(max_length=255, blank=True, null=True)
    agerestriction = models.CharField(max_length=255, blank=True, null=True)
    totalissues = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblioitems'


class BorrowerAttributeTypes(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    description = models.CharField(max_length=255)
    repeatable = models.IntegerField()
    unique_id = models.IntegerField()
    opac_display = models.IntegerField()
    opac_editable = models.IntegerField()
    staff_searchable = models.IntegerField()
    authorised_value_category = models.CharField(max_length=32, blank=True, null=True)
    display_checkout = models.IntegerField()
    category_code = models.CharField(max_length=10, blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=255)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'borrower_attribute_types'


class BorrowerAttributeTypesBranches(models.Model):
    bat_code = models.ForeignKey(BorrowerAttributeTypes, models.DO_NOTHING, db_column='bat_code', blank=True, null=True)
    b_branchcode = models.ForeignKey('Branches', models.DO_NOTHING, db_column='b_branchcode', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'borrower_attribute_types_branches'


class BorrowerAttributes(models.Model):
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber')
    code = models.ForeignKey(BorrowerAttributeTypes, models.DO_NOTHING, db_column='code')
    attribute = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'borrower_attributes'


class BorrowerDebarments(models.Model):
    borrower_debarment_id = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber')
    expiration = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=10)
    comment = models.TextField(blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'borrower_debarments'


class BorrowerFiles(models.Model):
    file_id = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    file_description = models.CharField(max_length=255, blank=True, null=True)
    file_content = models.TextField()
    date_uploaded = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'borrower_files'


class BorrowerMessagePreferences(models.Model):
    borrower_message_preference_id = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey('Borrowers', models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    categorycode = models.ForeignKey('Categories', models.DO_NOTHING, db_column='categorycode', blank=True, null=True)
    message_attribute = models.ForeignKey('MessageAttributes', models.DO_NOTHING, blank=True, null=True)
    days_in_advance = models.IntegerField(blank=True, null=True)
    wants_digest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'borrower_message_preferences'


class BorrowerMessageTransportPreferences(models.Model):
    borrower_message_preference = models.OneToOneField(BorrowerMessagePreferences, models.DO_NOTHING, primary_key=True)
    message_transport_type = models.ForeignKey('MessageTransportTypes', models.DO_NOTHING, db_column='message_transport_type')

    class Meta:
        managed = False
        db_table = 'borrower_message_transport_preferences'
        unique_together = (('borrower_message_preference', 'message_transport_type'),)


class BorrowerModifications(models.Model):
    timestamp = models.DateTimeField()
    verification_token = models.CharField(primary_key=True, max_length=255)
    borrowernumber = models.IntegerField()
    cardnumber = models.CharField(max_length=32, blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    othernames = models.TextField(blank=True, null=True)
    initials = models.TextField(blank=True, null=True)
    streetnumber = models.CharField(max_length=10, blank=True, null=True)
    streettype = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zipcode = models.CharField(max_length=25, blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    emailpro = models.TextField(blank=True, null=True)
    phonepro = models.TextField(blank=True, null=True)
    b_streetnumber = models.CharField(db_column='B_streetnumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    b_streettype = models.CharField(db_column='B_streettype', max_length=50, blank=True, null=True)  # Field name made lowercase.
    b_address = models.CharField(db_column='B_address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    b_address2 = models.TextField(db_column='B_address2', blank=True, null=True)  # Field name made lowercase.
    b_city = models.TextField(db_column='B_city', blank=True, null=True)  # Field name made lowercase.
    b_state = models.TextField(db_column='B_state', blank=True, null=True)  # Field name made lowercase.
    b_zipcode = models.CharField(db_column='B_zipcode', max_length=25, blank=True, null=True)  # Field name made lowercase.
    b_country = models.TextField(db_column='B_country', blank=True, null=True)  # Field name made lowercase.
    b_email = models.TextField(db_column='B_email', blank=True, null=True)  # Field name made lowercase.
    b_phone = models.TextField(db_column='B_phone', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(blank=True, null=True)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    categorycode = models.CharField(max_length=10, blank=True, null=True)
    dateenrolled = models.DateField(blank=True, null=True)
    dateexpiry = models.DateField(blank=True, null=True)
    date_renewed = models.DateField(blank=True, null=True)
    gonenoaddress = models.IntegerField(blank=True, null=True)
    lost = models.IntegerField(blank=True, null=True)
    debarred = models.DateField(blank=True, null=True)
    debarredcomment = models.CharField(max_length=255, blank=True, null=True)
    contactname = models.TextField(blank=True, null=True)
    contactfirstname = models.TextField(blank=True, null=True)
    contacttitle = models.TextField(blank=True, null=True)
    guarantorid = models.IntegerField(blank=True, null=True)
    borrowernotes = models.TextField(blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    userid = models.CharField(max_length=75, blank=True, null=True)
    opacnote = models.TextField(blank=True, null=True)
    contactnote = models.CharField(max_length=255, blank=True, null=True)
    sort1 = models.CharField(max_length=80, blank=True, null=True)
    sort2 = models.CharField(max_length=80, blank=True, null=True)
    altcontactfirstname = models.CharField(max_length=255, blank=True, null=True)
    altcontactsurname = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress1 = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress2 = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress3 = models.CharField(max_length=255, blank=True, null=True)
    altcontactstate = models.TextField(blank=True, null=True)
    altcontactzipcode = models.CharField(max_length=50, blank=True, null=True)
    altcontactcountry = models.TextField(blank=True, null=True)
    altcontactphone = models.CharField(max_length=50, blank=True, null=True)
    smsalertnumber = models.CharField(max_length=50, blank=True, null=True)
    privacy = models.IntegerField(blank=True, null=True)
    extended_attributes = models.TextField(blank=True, null=True)
    gdpr_proc_consent = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'borrower_modifications'
        unique_together = (('verification_token', 'borrowernumber'),)


class BorrowerPasswordRecovery(models.Model):
    borrowernumber = models.IntegerField(primary_key=True)
    uuid = models.CharField(max_length=128)
    valid_until = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'borrower_password_recovery'


class Borrowers(models.Model):
    borrowernumber = models.AutoField(primary_key=True)
    cardnumber = models.CharField(unique=True, max_length=32, blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    othernames = models.TextField(blank=True, null=True)
    initials = models.TextField(blank=True, null=True)
    streetnumber = models.CharField(max_length=10, blank=True, null=True)
    streettype = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zipcode = models.CharField(max_length=25, blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    emailpro = models.TextField(blank=True, null=True)
    phonepro = models.TextField(blank=True, null=True)
    b_streetnumber = models.CharField(db_column='B_streetnumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    b_streettype = models.CharField(db_column='B_streettype', max_length=50, blank=True, null=True)  # Field name made lowercase.
    b_address = models.CharField(db_column='B_address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    b_address2 = models.TextField(db_column='B_address2', blank=True, null=True)  # Field name made lowercase.
    b_city = models.TextField(db_column='B_city', blank=True, null=True)  # Field name made lowercase.
    b_state = models.TextField(db_column='B_state', blank=True, null=True)  # Field name made lowercase.
    b_zipcode = models.CharField(db_column='B_zipcode', max_length=25, blank=True, null=True)  # Field name made lowercase.
    b_country = models.TextField(db_column='B_country', blank=True, null=True)  # Field name made lowercase.
    b_email = models.TextField(db_column='B_email', blank=True, null=True)  # Field name made lowercase.
    b_phone = models.TextField(db_column='B_phone', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(blank=True, null=True)
    branchcode = models.ForeignKey('Branches', models.DO_NOTHING, db_column='branchcode')
    categorycode = models.ForeignKey('Categories', models.DO_NOTHING, db_column='categorycode')
    dateenrolled = models.DateField(blank=True, null=True)
    dateexpiry = models.DateField(blank=True, null=True)
    date_renewed = models.DateField(blank=True, null=True)
    gonenoaddress = models.IntegerField(blank=True, null=True)
    lost = models.IntegerField(blank=True, null=True)
    debarred = models.DateField(blank=True, null=True)
    debarredcomment = models.CharField(max_length=255, blank=True, null=True)
    contactname = models.TextField(blank=True, null=True)
    contactfirstname = models.TextField(blank=True, null=True)
    contacttitle = models.TextField(blank=True, null=True)
    guarantorid = models.IntegerField(blank=True, null=True)
    borrowernotes = models.TextField(blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    userid = models.CharField(unique=True, max_length=75, blank=True, null=True)
    opacnote = models.TextField(blank=True, null=True)
    contactnote = models.CharField(max_length=255, blank=True, null=True)
    sort1 = models.CharField(max_length=80, blank=True, null=True)
    sort2 = models.CharField(max_length=80, blank=True, null=True)
    altcontactfirstname = models.CharField(max_length=255, blank=True, null=True)
    altcontactsurname = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress1 = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress2 = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress3 = models.CharField(max_length=255, blank=True, null=True)
    altcontactstate = models.TextField(blank=True, null=True)
    altcontactzipcode = models.CharField(max_length=50, blank=True, null=True)
    altcontactcountry = models.TextField(blank=True, null=True)
    altcontactphone = models.CharField(max_length=50, blank=True, null=True)
    smsalertnumber = models.CharField(max_length=50, blank=True, null=True)
    sms_provider = models.ForeignKey('SmsProviders', models.DO_NOTHING, blank=True, null=True)
    privacy = models.IntegerField()
    privacy_guarantor_checkouts = models.IntegerField()
    checkprevcheckout = models.CharField(max_length=7)
    updated_on = models.DateTimeField()
    lastseen = models.DateTimeField(blank=True, null=True)
    lang = models.CharField(max_length=25, blank=True)
    login_attempts = models.IntegerField(blank=True, null=True)
    overdrive_auth_token = models.TextField(blank=True, null=True)

    @property
    def full_name(self):
        fullname = ""
        if self.firstname:
            fullname += self.firstname
            if self.surname:
                fullname += " " + self.surname
        elif self.surname:
            fullname += self.surname

        return fullname

    class Meta:
        verbose_name_plural = 'Borrowers'
        managed = False
        db_table = 'borrowers'

    def __str__(self):
            return str(self.borrowernumber) + ' - ' + self.firstname + self.surname if self.firstname else str(self.borrowernumber) + ' - ' +  self.surname


class BranchBorrowerCircRules(models.Model):
    categorycode = models.OneToOneField('Categories', models.DO_NOTHING, db_column='categorycode', primary_key=True)
    branchcode = models.ForeignKey('Branches', models.DO_NOTHING, db_column='branchcode')
    maxissueqty = models.IntegerField(blank=True, null=True)
    maxonsiteissueqty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch_borrower_circ_rules'
        unique_together = (('categorycode', 'branchcode'),)


class BranchItemRules(models.Model):
    itemtype = models.OneToOneField('Itemtypes', models.DO_NOTHING, db_column='itemtype', primary_key=True)
    branchcode = models.ForeignKey('Branches', models.DO_NOTHING, db_column='branchcode')
    holdallowed = models.IntegerField(blank=True, null=True)
    hold_fulfillment_policy = models.CharField(max_length=13)
    returnbranch = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch_item_rules'
        unique_together = (('itemtype', 'branchcode'),)


class BranchTransferLimits(models.Model):
    limitid = models.AutoField(db_column='limitId', primary_key=True)  # Field name made lowercase.
    tobranch = models.CharField(db_column='toBranch', max_length=10)  # Field name made lowercase.
    frombranch = models.CharField(db_column='fromBranch', max_length=10)  # Field name made lowercase.
    itemtype = models.CharField(max_length=10, blank=True, null=True)
    ccode = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch_transfer_limits'


class Branches(models.Model):
    branchcode = models.CharField(primary_key=True, max_length=10)
    branchname = models.TextField()
    branchaddress1 = models.TextField(blank=True, null=True)
    branchaddress2 = models.TextField(blank=True, null=True)
    branchaddress3 = models.TextField(blank=True, null=True)
    branchzip = models.CharField(max_length=25, blank=True, null=True)
    branchcity = models.TextField(blank=True, null=True)
    branchstate = models.TextField(blank=True, null=True)
    branchcountry = models.TextField(blank=True, null=True)
    branchphone = models.TextField(blank=True, null=True)
    branchfax = models.TextField(blank=True, null=True)
    branchemail = models.TextField(blank=True, null=True)
    branchreplyto = models.TextField(blank=True, null=True)
    branchreturnpath = models.TextField(blank=True, null=True)
    branchurl = models.TextField(blank=True, null=True)
    issuing = models.IntegerField(blank=True, null=True)
    branchip = models.CharField(max_length=15, blank=True, null=True)
    branchprinter = models.CharField(max_length=100, blank=True, null=True)
    branchnotes = models.TextField(blank=True, null=True)
    opac_info = models.TextField(blank=True, null=True)
    geolocation = models.CharField(max_length=255, blank=True, null=True)
    marcorgcode = models.CharField(max_length=16, blank=True, null=True)
    pickup_location = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Branches'
        managed = False
        db_table = 'branches'

    def __str__(self):
        return self.branchname + ' - ' + self.branchcode


class BranchesOverdrive(models.Model):
    branchcode = models.OneToOneField(Branches, models.DO_NOTHING, db_column='branchcode', primary_key=True)
    authname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'branches_overdrive'


class Branchtransfers(models.Model):
    branchtransfer_id = models.AutoField(primary_key=True)
    itemnumber = models.ForeignKey('Items', models.DO_NOTHING, db_column='itemnumber')
    datesent = models.DateTimeField(blank=True, null=True)
    frombranch = models.ForeignKey(Branches, models.DO_NOTHING, related_name='transfers_given', db_column='frombranch')
    datearrived = models.DateTimeField(blank=True, null=True)
    tobranch = models.ForeignKey(Branches, models.DO_NOTHING, related_name='transfers_received', db_column='tobranch')
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branchtransfers'


class Browser(models.Model):
    level = models.IntegerField()
    classification = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    number = models.BigIntegerField()
    endnode = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'browser'


class Categories(models.Model):
    ''' Category for patrons '''
    categorycode = models.CharField(primary_key=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    enrolmentperiod = models.SmallIntegerField(blank=True, null=True)
    enrolmentperioddate = models.DateField(blank=True, null=True)
    upperagelimit = models.SmallIntegerField(blank=True, null=True)
    dateofbirthrequired = models.IntegerField(blank=True, null=True)
    finetype = models.CharField(max_length=30, blank=True, null=True)
    bulk = models.IntegerField(blank=True, null=True)
    enrolmentfee = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    overduenoticerequired = models.IntegerField(blank=True, null=True)
    issuelimit = models.SmallIntegerField(blank=True, null=True)
    reservefee = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    hidelostitems = models.IntegerField()
    category_type = models.CharField(max_length=1)
    blockexpiredpatronopacactions = models.IntegerField(db_column='BlockExpiredPatronOpacActions')  # Field name made lowercase.
    default_privacy = models.CharField(max_length=7)
    checkprevcheckout = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = 'Categories'
        managed = False
        db_table = 'categories'

    def __str__(self):
        return self.categorycode


class CategoriesBranches(models.Model):
    categorycode = models.ForeignKey(Categories, models.DO_NOTHING, db_column='categorycode', blank=True, null=True)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories_branches'


class CirculationRules(models.Model):
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    categorycode = models.ForeignKey(Categories, models.DO_NOTHING, db_column='categorycode', blank=True, null=True)
    itemtype = models.ForeignKey('Itemtypes', models.DO_NOTHING, db_column='itemtype', blank=True, null=True)
    rule_name = models.CharField(max_length=32)
    rule_value = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'circulation_rules'
        unique_together = (('branchcode', 'categorycode', 'itemtype', 'rule_name'),)


class Cities(models.Model):
    cityid = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    city_state = models.CharField(max_length=100, blank=True, null=True)
    city_country = models.CharField(max_length=100, blank=True, null=True)
    city_zipcode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'


class ClassSortRules(models.Model):
    class_sort_rule = models.CharField(primary_key=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    sort_routine = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'class_sort_rules'


class ClassSources(models.Model):
    cn_source = models.CharField(primary_key=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    used = models.IntegerField()
    class_sort_rule = models.ForeignKey(ClassSortRules, models.DO_NOTHING, db_column='class_sort_rule')
    class_split_rule = models.ForeignKey('ClassSplitRules', models.DO_NOTHING, db_column='class_split_rule')

    class Meta:
        managed = False
        db_table = 'class_sources'


class ClassSplitRules(models.Model):
    class_split_rule = models.CharField(primary_key=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    split_routine = models.CharField(max_length=30)
    split_regex = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'class_split_rules'


class ClubEnrollmentFields(models.Model):
    club_enrollment = models.ForeignKey('ClubEnrollments', models.DO_NOTHING)
    club_template_enrollment_field = models.ForeignKey('ClubTemplateEnrollmentFields', models.DO_NOTHING)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'club_enrollment_fields'


class ClubEnrollments(models.Model):
    club = models.ForeignKey('Clubs', models.DO_NOTHING)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')
    date_enrolled = models.DateTimeField()
    date_canceled = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'club_enrollments'


class ClubFields(models.Model):
    club_template_field = models.ForeignKey('ClubTemplateFields', models.DO_NOTHING)
    club = models.ForeignKey('Clubs', models.DO_NOTHING)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'club_fields'


class ClubTemplateEnrollmentFields(models.Model):
    club_template = models.ForeignKey('ClubTemplates', models.DO_NOTHING)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    authorised_value_category = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'club_template_enrollment_fields'


class ClubTemplateFields(models.Model):
    club_template = models.ForeignKey('ClubTemplates', models.DO_NOTHING)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    authorised_value_category = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'club_template_fields'


class ClubTemplates(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    is_enrollable_from_opac = models.IntegerField()
    is_email_required = models.IntegerField()
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)
    is_deletable = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'club_templates'


class Clubs(models.Model):
    club_template = models.ForeignKey(ClubTemplates, models.DO_NOTHING)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clubs'


class Collections(models.Model):
    colid = models.AutoField(db_column='colId', primary_key=True)  # Field name made lowercase.
    coltitle = models.CharField(db_column='colTitle', max_length=100)  # Field name made lowercase.
    coldesc = models.TextField(db_column='colDesc')  # Field name made lowercase.
    colbranchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='colBranchcode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'collections'


class CollectionsTracking(models.Model):
    collections_tracking_id = models.AutoField(primary_key=True)
    colid = models.IntegerField(db_column='colId')  # Field name made lowercase.
    itemnumber = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'collections_tracking'


class ColumnsSettings(models.Model):
    module = models.CharField(primary_key=True, max_length=255)
    page = models.CharField(max_length=255)
    tablename = models.CharField(max_length=255)
    columnname = models.CharField(max_length=255)
    cannot_be_toggled = models.IntegerField()
    is_hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'columns_settings'
        unique_together = (('module', 'page', 'tablename', 'columnname'),)


class CourseInstructors(models.Model):
    course = models.OneToOneField('Courses', models.DO_NOTHING, primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')

    class Meta:
        managed = False
        db_table = 'course_instructors'
        unique_together = (('course', 'borrowernumber'),)


class CourseItems(models.Model):
    ci_id = models.AutoField(primary_key=True)
    itemnumber = models.OneToOneField('Items', models.DO_NOTHING, db_column='itemnumber', unique=True)
    itype = models.CharField(max_length=10, blank=True, null=True)
    ccode = models.CharField(max_length=80, blank=True, null=True)
    holdingbranch = models.ForeignKey(Branches, models.DO_NOTHING, db_column='holdingbranch', blank=True, null=True)
    location = models.CharField(max_length=80, blank=True, null=True)
    enabled = models.CharField(max_length=3)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'course_items'


class CourseReserves(models.Model):
    cr_id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Courses', models.DO_NOTHING)
    ci = models.ForeignKey(CourseItems, models.DO_NOTHING)
    staff_note = models.TextField(blank=True, null=True)
    public_note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'course_reserves'
        unique_together = (('course', 'ci'),)


class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=80, blank=True, null=True)
    course_number = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    course_name = models.CharField(max_length=255, blank=True, null=True)
    term = models.CharField(max_length=80, blank=True, null=True)
    staff_note = models.TextField(blank=True, null=True)
    public_note = models.TextField(blank=True, null=True)
    students_count = models.CharField(max_length=20, blank=True, null=True)
    enabled = models.CharField(max_length=3)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'courses'


class CreatorBatches(models.Model):
    label_id = models.AutoField(primary_key=True)
    batch_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    item_number = models.ForeignKey('Items', models.DO_NOTHING, db_column='item_number', blank=True, null=True)
    borrower_number = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrower_number', blank=True, null=True)
    timestamp = models.DateTimeField()
    branch_code = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branch_code')
    creator = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'creator_batches'


class CreatorImages(models.Model):
    image_id = models.AutoField(primary_key=True)
    imagefile = models.TextField(blank=True, null=True)
    image_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'creator_images'


class CreatorLayouts(models.Model):
    layout_id = models.AutoField(primary_key=True)
    barcode_type = models.CharField(max_length=100)
    start_label = models.IntegerField()
    printing_type = models.CharField(max_length=32)
    layout_name = models.CharField(max_length=25)
    guidebox = models.IntegerField(blank=True, null=True)
    oblique_title = models.IntegerField(blank=True, null=True)
    font = models.CharField(max_length=10)
    font_size = models.IntegerField()
    units = models.CharField(max_length=20)
    callnum_split = models.IntegerField(blank=True, null=True)
    text_justify = models.CharField(max_length=1)
    format_string = models.CharField(max_length=210)
    layout_xml = models.TextField()
    creator = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'creator_layouts'


class CreatorTemplates(models.Model):
    template_id = models.AutoField(primary_key=True)
    profile_id = models.IntegerField(blank=True, null=True)
    template_code = models.CharField(max_length=100)
    template_desc = models.CharField(max_length=100)
    page_width = models.FloatField()
    page_height = models.FloatField()
    label_width = models.FloatField()
    label_height = models.FloatField()
    top_text_margin = models.FloatField()
    left_text_margin = models.FloatField()
    top_margin = models.FloatField()
    left_margin = models.FloatField()
    cols = models.IntegerField()
    rows = models.IntegerField()
    col_gap = models.FloatField()
    row_gap = models.FloatField()
    units = models.CharField(max_length=20)
    creator = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'creator_templates'


class Currency(models.Model):
    currency = models.CharField(primary_key=True, max_length=10)
    symbol = models.CharField(max_length=5, blank=True, null=True)
    isocode = models.CharField(max_length=5, blank=True, null=True)
    timestamp = models.DateTimeField()
    rate = models.FloatField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    archived = models.IntegerField(blank=True, null=True)
    p_sep_by_space = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'currency'


class DefaultBorrowerCircRules(models.Model):
    categorycode = models.OneToOneField(Categories, models.DO_NOTHING, db_column='categorycode', primary_key=True)
    maxissueqty = models.IntegerField(blank=True, null=True)
    maxonsiteissueqty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'default_borrower_circ_rules'


class DefaultBranchCircRules(models.Model):
    branchcode = models.OneToOneField(Branches, models.DO_NOTHING, db_column='branchcode', primary_key=True)
    maxissueqty = models.IntegerField(blank=True, null=True)
    maxonsiteissueqty = models.IntegerField(blank=True, null=True)
    holdallowed = models.IntegerField(blank=True, null=True)
    hold_fulfillment_policy = models.CharField(max_length=13)
    returnbranch = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'default_branch_circ_rules'


class DefaultBranchItemRules(models.Model):
    itemtype = models.OneToOneField('Itemtypes', models.DO_NOTHING, db_column='itemtype', primary_key=True)
    holdallowed = models.IntegerField(blank=True, null=True)
    hold_fulfillment_policy = models.CharField(max_length=13)
    returnbranch = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'default_branch_item_rules'


class DefaultCircRules(models.Model):
    singleton = models.CharField(primary_key=True, max_length=9)
    maxissueqty = models.IntegerField(blank=True, null=True)
    maxonsiteissueqty = models.IntegerField(blank=True, null=True)
    holdallowed = models.IntegerField(blank=True, null=True)
    hold_fulfillment_policy = models.CharField(max_length=13)
    returnbranch = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'default_circ_rules'


class Deletedbiblio(models.Model):
    biblionumber = models.AutoField(primary_key=True)
    frameworkcode = models.CharField(max_length=4)
    author = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    unititle = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    serial = models.IntegerField(blank=True, null=True)
    seriestitle = models.TextField(blank=True, null=True)
    copyrightdate = models.SmallIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()
    datecreated = models.DateField()
    abstract = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deletedbiblio'


class DeletedbiblioMetadata(models.Model):
    biblionumber = models.ForeignKey(Deletedbiblio, models.DO_NOTHING, db_column='biblionumber')
    format = models.CharField(max_length=16)
    marcflavour = models.CharField(max_length=16)
    metadata = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'deletedbiblio_metadata'
        unique_together = (('biblionumber', 'format', 'marcflavour'),)


class Deletedbiblioitems(models.Model):
    biblioitemnumber = models.IntegerField(primary_key=True)
    biblionumber = models.IntegerField()
    volume = models.TextField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)
    itemtype = models.CharField(max_length=10, blank=True, null=True)
    isbn = models.TextField(blank=True, null=True)
    issn = models.TextField(blank=True, null=True)
    ean = models.TextField(blank=True, null=True)
    publicationyear = models.TextField(blank=True, null=True)
    publishercode = models.CharField(max_length=255, blank=True, null=True)
    volumedate = models.DateField(blank=True, null=True)
    volumedesc = models.TextField(blank=True, null=True)
    collectiontitle = models.TextField(blank=True, null=True)
    collectionissn = models.TextField(blank=True, null=True)
    collectionvolume = models.TextField(blank=True, null=True)
    editionstatement = models.TextField(blank=True, null=True)
    editionresponsibility = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    illus = models.CharField(max_length=255, blank=True, null=True)
    pages = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    lccn = models.CharField(max_length=25, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    cn_source = models.CharField(max_length=10, blank=True, null=True)
    cn_class = models.CharField(max_length=30, blank=True, null=True)
    cn_item = models.CharField(max_length=10, blank=True, null=True)
    cn_suffix = models.CharField(max_length=10, blank=True, null=True)
    cn_sort = models.CharField(max_length=255, blank=True, null=True)
    agerestriction = models.CharField(max_length=255, blank=True, null=True)
    totalissues = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deletedbiblioitems'


class Deletedborrowers(models.Model):
    borrowernumber = models.IntegerField(primary_key=True)
    cardnumber = models.CharField(max_length=32, blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    othernames = models.TextField(blank=True, null=True)
    initials = models.TextField(blank=True, null=True)
    streetnumber = models.CharField(max_length=10, blank=True, null=True)
    streettype = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zipcode = models.CharField(max_length=25, blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    emailpro = models.TextField(blank=True, null=True)
    phonepro = models.TextField(blank=True, null=True)
    b_streetnumber = models.CharField(db_column='B_streetnumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    b_streettype = models.CharField(db_column='B_streettype', max_length=50, blank=True, null=True)  # Field name made lowercase.
    b_address = models.CharField(db_column='B_address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    b_address2 = models.TextField(db_column='B_address2', blank=True, null=True)  # Field name made lowercase.
    b_city = models.TextField(db_column='B_city', blank=True, null=True)  # Field name made lowercase.
    b_state = models.TextField(db_column='B_state', blank=True, null=True)  # Field name made lowercase.
    b_zipcode = models.CharField(db_column='B_zipcode', max_length=25, blank=True, null=True)  # Field name made lowercase.
    b_country = models.TextField(db_column='B_country', blank=True, null=True)  # Field name made lowercase.
    b_email = models.TextField(db_column='B_email', blank=True, null=True)  # Field name made lowercase.
    b_phone = models.TextField(db_column='B_phone', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(blank=True, null=True)
    branchcode = models.CharField(max_length=10)
    categorycode = models.CharField(max_length=10)
    dateenrolled = models.DateField(blank=True, null=True)
    dateexpiry = models.DateField(blank=True, null=True)
    date_renewed = models.DateField(blank=True, null=True)
    gonenoaddress = models.IntegerField(blank=True, null=True)
    lost = models.IntegerField(blank=True, null=True)
    debarred = models.DateField(blank=True, null=True)
    debarredcomment = models.CharField(max_length=255, blank=True, null=True)
    contactname = models.TextField(blank=True, null=True)
    contactfirstname = models.TextField(blank=True, null=True)
    contacttitle = models.TextField(blank=True, null=True)
    guarantorid = models.IntegerField(blank=True, null=True)
    borrowernotes = models.TextField(blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    userid = models.CharField(max_length=75, blank=True, null=True)
    opacnote = models.TextField(blank=True, null=True)
    contactnote = models.CharField(max_length=255, blank=True, null=True)
    sort1 = models.CharField(max_length=80, blank=True, null=True)
    sort2 = models.CharField(max_length=80, blank=True, null=True)
    altcontactfirstname = models.CharField(max_length=255, blank=True, null=True)
    altcontactsurname = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress1 = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress2 = models.CharField(max_length=255, blank=True, null=True)
    altcontactaddress3 = models.CharField(max_length=255, blank=True, null=True)
    altcontactstate = models.TextField(blank=True, null=True)
    altcontactzipcode = models.CharField(max_length=50, blank=True, null=True)
    altcontactcountry = models.TextField(blank=True, null=True)
    altcontactphone = models.CharField(max_length=50, blank=True, null=True)
    smsalertnumber = models.CharField(max_length=50, blank=True, null=True)
    sms_provider_id = models.IntegerField(blank=True, null=True)
    privacy = models.IntegerField()
    privacy_guarantor_checkouts = models.IntegerField()
    checkprevcheckout = models.CharField(max_length=7)
    updated_on = models.DateTimeField()
    lastseen = models.DateTimeField(blank=True, null=True)
    lang = models.CharField(max_length=25)
    login_attempts = models.IntegerField(blank=True, null=True)
    overdrive_auth_token = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deletedborrowers'


class Deleteditems(models.Model):
    itemnumber = models.IntegerField(primary_key=True)
    biblionumber = models.IntegerField()
    biblioitemnumber = models.IntegerField()
    barcode = models.CharField(max_length=20, blank=True, null=True)
    dateaccessioned = models.DateField(blank=True, null=True)
    booksellerid = models.TextField(blank=True, null=True)
    homebranch = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    replacementprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    replacementpricedate = models.DateField(blank=True, null=True)
    datelastborrowed = models.DateField(blank=True, null=True)
    datelastseen = models.DateField(blank=True, null=True)
    stack = models.IntegerField(blank=True, null=True)
    notforloan = models.IntegerField()
    damaged = models.IntegerField()
    damaged_on = models.DateTimeField(blank=True, null=True)
    itemlost = models.IntegerField()
    itemlost_on = models.DateTimeField(blank=True, null=True)
    withdrawn = models.IntegerField()
    withdrawn_on = models.DateTimeField(blank=True, null=True)
    itemcallnumber = models.CharField(max_length=255, blank=True, null=True)
    coded_location_qualifier = models.CharField(max_length=10, blank=True, null=True)
    issues = models.SmallIntegerField(blank=True, null=True)
    renewals = models.SmallIntegerField(blank=True, null=True)
    reserves = models.SmallIntegerField(blank=True, null=True)
    restricted = models.IntegerField(blank=True, null=True)
    itemnotes = models.TextField(blank=True, null=True)
    itemnotes_nonpublic = models.TextField(blank=True, null=True)
    holdingbranch = models.CharField(max_length=10, blank=True, null=True)
    paidfor = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    location = models.CharField(max_length=80, blank=True, null=True)
    permanent_location = models.CharField(max_length=80, blank=True, null=True)
    onloan = models.DateField(blank=True, null=True)
    cn_source = models.CharField(max_length=10, blank=True, null=True)
    cn_sort = models.CharField(max_length=255, blank=True, null=True)
    ccode = models.CharField(max_length=80, blank=True, null=True)
    materials = models.TextField(blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    itype = models.CharField(max_length=10, blank=True, null=True)
    more_subfields_xml = models.TextField(blank=True, null=True)
    enumchron = models.TextField(blank=True, null=True)
    copynumber = models.CharField(max_length=32, blank=True, null=True)
    stocknumber = models.CharField(max_length=32, blank=True, null=True)
    new_status = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deleteditems'


class Discharges(models.Model):
    discharge_id = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrower', blank=True, null=True)
    needed = models.DateTimeField(blank=True, null=True)
    validated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discharges'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EdifactEan(models.Model):
    ee_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=128, blank=True, null=True)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    ean = models.CharField(max_length=15)
    id_code_qualifier = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'edifact_ean'


class EdifactMessages(models.Model):
    message_type = models.CharField(max_length=10)
    transfer_date = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(Aqbooksellers, models.DO_NOTHING, blank=True, null=True)
    edi_acct = models.ForeignKey('VendorEdiAccounts', models.DO_NOTHING, db_column='edi_acct', blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    basketno = models.ForeignKey(Aqbasket, models.DO_NOTHING, db_column='basketno', blank=True, null=True)
    raw_msg = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'edifact_messages'


class ExportFormat(models.Model):
    export_format_id = models.AutoField(primary_key=True)
    profile = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    csv_separator = models.CharField(max_length=2)
    field_separator = models.CharField(max_length=2, blank=True, null=True)
    subfield_separator = models.CharField(max_length=2, blank=True, null=True)
    encoding = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    used_for = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'export_format'


class Fieldmapping(models.Model):
    field = models.CharField(max_length=255)
    frameworkcode = models.CharField(max_length=4)
    fieldcode = models.CharField(max_length=3)
    subfieldcode = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'fieldmapping'


class HoldFillTargets(models.Model):
    itemnumber = models.OneToOneField('Items', models.DO_NOTHING, db_column='itemnumber', primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    source_branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='source_branchcode', blank=True, null=True)
    item_level_request = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hold_fill_targets'


class HouseboundProfile(models.Model):
    borrowernumber = models.OneToOneField(Borrowers, models.DO_NOTHING, db_column='borrowernumber', primary_key=True)
    day = models.TextField()
    frequency = models.TextField()
    fav_itemtypes = models.TextField(blank=True, null=True)
    fav_subjects = models.TextField(blank=True, null=True)
    fav_authors = models.TextField(blank=True, null=True)
    referral = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'housebound_profile'


class HouseboundRole(models.Model):
    borrowernumber = models.OneToOneField(Borrowers, models.DO_NOTHING, primary_key=True)
    housebound_chooser = models.IntegerField()
    housebound_deliverer = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'housebound_role'


class HouseboundVisit(models.Model):
    borrowernumber = models.ForeignKey(HouseboundProfile, models.DO_NOTHING, db_column='borrowernumber')
    appointment_date = models.DateField(blank=True, null=True)
    day_segment = models.CharField(max_length=10, blank=True, null=True)
    chooser_brwnumber = models.ForeignKey(Borrowers, models.DO_NOTHING, related_name='visits_chosen', db_column='chooser_brwnumber', blank=True, null=True) # Borrower to choose items for delivery.
    deliverer_brwnumber = models.ForeignKey(Borrowers, models.DO_NOTHING, related_name='visits_received', db_column='deliverer_brwnumber', blank=True, null=True) # Borrower to deliver items to.

    class Meta:
        managed = False
        db_table = 'housebound_visit'


class Illcomments(models.Model):
    illcomment_id = models.AutoField(primary_key=True)
    illrequest = models.ForeignKey('Illrequests', models.DO_NOTHING)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'illcomments'


class Illrequestattributes(models.Model):
    illrequest = models.OneToOneField('Illrequests', models.DO_NOTHING, primary_key=True)
    type = models.CharField(max_length=200)
    value = models.TextField()
    readonly = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'illrequestattributes'
        unique_together = (('illrequest', 'type'),)


class Illrequests(models.Model):
    illrequest_id = models.BigAutoField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    biblio_id = models.IntegerField(blank=True, null=True)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode')
    status = models.CharField(max_length=50, blank=True, null=True)
    placed = models.DateField(blank=True, null=True)
    replied = models.DateField(blank=True, null=True)
    updated = models.DateTimeField()
    completed = models.DateField(blank=True, null=True)
    medium = models.CharField(max_length=30, blank=True, null=True)
    accessurl = models.CharField(max_length=500, blank=True, null=True)
    cost = models.CharField(max_length=20, blank=True, null=True)
    price_paid = models.CharField(max_length=20, blank=True, null=True)
    notesopac = models.TextField(blank=True, null=True)
    notesstaff = models.TextField(blank=True, null=True)
    orderid = models.CharField(max_length=50, blank=True, null=True)
    backend = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'illrequests'


class ImportAuths(models.Model):
    import_record = models.ForeignKey('ImportRecords', models.DO_NOTHING)
    matched_authid = models.IntegerField(blank=True, null=True)
    control_number = models.CharField(max_length=25, blank=True, null=True)
    authorized_heading = models.CharField(max_length=128, blank=True, null=True)
    original_source = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_auths'


class ImportBatches(models.Model):
    import_batch_id = models.AutoField(primary_key=True)
    matcher_id = models.IntegerField(blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    num_records = models.IntegerField()
    num_items = models.IntegerField()
    upload_timestamp = models.DateTimeField()
    overlay_action = models.CharField(max_length=12)
    nomatch_action = models.CharField(max_length=10)
    item_action = models.CharField(max_length=20)
    import_status = models.CharField(max_length=9)
    batch_type = models.CharField(max_length=10)
    record_type = models.CharField(max_length=8)
    file_name = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_batches'


class ImportBiblios(models.Model):
    import_record = models.ForeignKey('ImportRecords', models.DO_NOTHING)
    matched_biblionumber = models.IntegerField(blank=True, null=True)
    control_number = models.CharField(max_length=25, blank=True, null=True)
    original_source = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    author = models.CharField(max_length=80, blank=True, null=True)
    isbn = models.CharField(max_length=30, blank=True, null=True)
    issn = models.CharField(max_length=9, blank=True, null=True)
    has_items = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'import_biblios'


class ImportItems(models.Model):
    import_items_id = models.AutoField(primary_key=True)
    import_record = models.ForeignKey('ImportRecords', models.DO_NOTHING)
    itemnumber = models.IntegerField(blank=True, null=True)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=8)
    marcxml = models.TextField()
    import_error = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_items'


class ImportRecordMatches(models.Model):
    import_record = models.ForeignKey('ImportRecords', models.DO_NOTHING)
    candidate_match_id = models.IntegerField()
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'import_record_matches'


class ImportRecords(models.Model):
    import_record_id = models.AutoField(primary_key=True)
    import_batch = models.ForeignKey(ImportBatches, models.DO_NOTHING)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    record_sequence = models.IntegerField()
    upload_timestamp = models.DateTimeField()
    import_date = models.DateField(blank=True, null=True)
    marc = models.TextField()
    marcxml = models.TextField()
    marcxml_old = models.TextField()
    record_type = models.CharField(max_length=8)
    overlay_status = models.CharField(max_length=13)
    status = models.CharField(max_length=14)
    import_error = models.TextField(blank=True, null=True)
    encoding = models.CharField(max_length=40)
    z3950random = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_records'


class Issues(models.Model):
    issue_id = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    itemnumber = models.OneToOneField('Items', models.DO_NOTHING, related_name='issues_set', db_column='itemnumber', unique=True, blank=True, null=True)
    date_due = models.DateTimeField(blank=True, null=True)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    returndate = models.DateTimeField(blank=True, null=True)
    lastreneweddate = models.DateTimeField(blank=True, null=True)
    renewals = models.IntegerField(blank=True, null=True)
    auto_renew = models.IntegerField(blank=True, null=True)
    auto_renew_error = models.CharField(max_length=32, blank=True, null=True)
    timestamp = models.DateTimeField()
    issuedate = models.DateTimeField(blank=True, null=True)
    onsite_checkout = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    notedate = models.DateTimeField(blank=True, null=True)
    noteseen = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issues'


class Issuingrules(models.Model):
    categorycode = models.CharField(max_length=10)
    itemtype = models.CharField(max_length=10)
    restrictedtype = models.IntegerField(blank=True, null=True)
    rentaldiscount = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    reservecharge = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    fine = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    finedays = models.IntegerField(blank=True, null=True)
    maxsuspensiondays = models.IntegerField(blank=True, null=True)
    suspension_chargeperiod = models.IntegerField(blank=True, null=True)
    firstremind = models.IntegerField(blank=True, null=True)
    chargeperiod = models.IntegerField(blank=True, null=True)
    chargeperiod_charge_at = models.IntegerField()
    accountsent = models.IntegerField(blank=True, null=True)
    chargename = models.CharField(max_length=100, blank=True, null=True)
    maxissueqty = models.IntegerField(blank=True, null=True)
    maxonsiteissueqty = models.IntegerField(blank=True, null=True)
    issuelength = models.IntegerField(blank=True, null=True)
    lengthunit = models.CharField(max_length=10, blank=True, null=True)
    hardduedate = models.DateField(blank=True, null=True)
    hardduedatecompare = models.IntegerField()
    renewalsallowed = models.SmallIntegerField()
    renewalperiod = models.IntegerField(blank=True, null=True)
    norenewalbefore = models.IntegerField(blank=True, null=True)
    auto_renew = models.IntegerField(blank=True, null=True)
    no_auto_renewal_after = models.IntegerField(blank=True, null=True)
    no_auto_renewal_after_hard_limit = models.DateField(blank=True, null=True)
    reservesallowed = models.SmallIntegerField()
    holds_per_record = models.SmallIntegerField()
    holds_per_day = models.SmallIntegerField(blank=True, null=True)
    branchcode = models.CharField(primary_key=True, max_length=10)
    overduefinescap = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    cap_fine_to_replacement_price = models.IntegerField()
    onshelfholds = models.IntegerField()
    opacitemholds = models.CharField(max_length=1)
    article_requests = models.CharField(max_length=9)
    note = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issuingrules'
        unique_together = (('branchcode', 'categorycode', 'itemtype'),)


class ItemCirculationAlertPreferences(models.Model):
    branchcode = models.CharField(max_length=10)
    categorycode = models.CharField(max_length=10)
    item_type = models.CharField(max_length=10)
    notification = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'item_circulation_alert_preferences'


class Items(models.Model):
    itemnumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    biblioitemnumber = models.ForeignKey(Biblioitems, models.DO_NOTHING, db_column='biblioitemnumber')
    barcode = models.CharField(unique=True, max_length=20, blank=True, null=True)
    dateaccessioned = models.DateField(blank=True, null=True)
    booksellerid = models.TextField(blank=True, null=True)
    homebranch = models.ForeignKey(Branches, models.DO_NOTHING, related_name='items_owned', db_column='homebranch', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    replacementprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    replacementpricedate = models.DateField(blank=True, null=True)
    datelastborrowed = models.DateField(blank=True, null=True)
    datelastseen = models.DateField(blank=True, null=True)
    stack = models.IntegerField(blank=True, null=True)
    notforloan = models.IntegerField()
    damaged = models.IntegerField()
    damaged_on = models.DateTimeField(blank=True, null=True)
    itemlost = models.IntegerField()
    itemlost_on = models.DateTimeField(blank=True, null=True)
    withdrawn = models.IntegerField()
    withdrawn_on = models.DateTimeField(blank=True, null=True)
    itemcallnumber = models.CharField(max_length=255, blank=True, null=True)
    coded_location_qualifier = models.CharField(max_length=10, blank=True, null=True)
    issues = models.SmallIntegerField(blank=True, null=True)
    renewals = models.SmallIntegerField(blank=True, null=True)
    reserves = models.SmallIntegerField(blank=True, null=True)
    restricted = models.IntegerField(blank=True, null=True)
    itemnotes = models.TextField(blank=True, null=True)
    itemnotes_nonpublic = models.TextField(blank=True, null=True)
    holdingbranch = models.ForeignKey(Branches, models.DO_NOTHING, db_column='holdingbranch', related_name='items_held', blank=True, null=True)
    paidfor = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    location = models.CharField(max_length=80, blank=True, null=True)
    permanent_location = models.CharField(max_length=80, blank=True, null=True)
    onloan = models.DateField(blank=True, null=True)
    cn_source = models.CharField(max_length=10, blank=True, null=True)
    cn_sort = models.CharField(max_length=255, blank=True, null=True)
    ccode = models.CharField(max_length=80, blank=True, null=True)
    materials = models.TextField(blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    itype = models.CharField(max_length=10, blank=True, null=True)
    more_subfields_xml = models.TextField(blank=True, null=True)
    enumchron = models.TextField(blank=True, null=True)
    copynumber = models.CharField(max_length=32, blank=True, null=True)
    stocknumber = models.CharField(max_length=32, blank=True, null=True)
    new_status = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'

    @property
    def full_title(self):
        import MySQLdb
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="igcarlibrary",
            db="library"
        )
        cur = db.cursor()
        sql_query = '''
            SELECT concat( biblio.title, ' ', ExtractValue((
                    SELECT metadata
                    FROM biblio_metadata b2
                    WHERE biblio.biblionumber = b2.biblionumber),
                      '//datafield[@tag="245"]/subfield[@code="b"]') )
            FROM biblio
            WHERE biblio.biblionumber = {}
            '''.format(self.biblionumber.biblionumber)
        try:
            cur.execute(sql_query)
        except:
            print(sql_query)
        return str(cur.fetchone()[0])

    def __str__(self):
        if self.barcode:
            return str(self.full_title) + ' - ' + str(self.barcode)
        else:
            return str(self.full_title)


class ItemsLastBorrower(models.Model):
    itemnumber = models.OneToOneField(Items, models.DO_NOTHING, db_column='itemnumber', unique=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'items_last_borrower'


class ItemsSearchFields(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    label = models.CharField(max_length=255)
    tagfield = models.CharField(max_length=3)
    tagsubfield = models.CharField(max_length=1, blank=True, null=True)
    authorised_values_category = models.ForeignKey(AuthorisedValueCategories, models.DO_NOTHING, db_column='authorised_values_category', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items_search_fields'


class Itemtypes(models.Model):
    itemtype = models.CharField(primary_key=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    rentalcharge = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    defaultreplacecost = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    processfee = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    notforloan = models.SmallIntegerField(blank=True, null=True)
    imageurl = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    checkinmsg = models.CharField(max_length=255, blank=True, null=True)
    checkinmsgtype = models.CharField(max_length=16)
    sip_media_type = models.CharField(max_length=3, blank=True, null=True)
    hideinopac = models.IntegerField()
    searchcategory = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itemtypes'


class LanguageDescriptions(models.Model):
    subtag = models.CharField(max_length=25, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    lang = models.CharField(max_length=25, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language_descriptions'


class LanguageRfc4646ToIso639(models.Model):
    rfc4646_subtag = models.CharField(max_length=25, blank=True, null=True)
    iso639_2_code = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language_rfc4646_to_iso639'


class LanguageScriptBidi(models.Model):
    rfc4646_subtag = models.CharField(max_length=25, blank=True, null=True)
    bidi = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language_script_bidi'


class LanguageScriptMapping(models.Model):
    language_subtag = models.CharField(max_length=25, blank=True, null=True)
    script_subtag = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language_script_mapping'


class LanguageSubtagRegistry(models.Model):
    subtag = models.CharField(max_length=25, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    description = models.CharField(max_length=25, blank=True, null=True)
    added = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language_subtag_registry'


class Letter(models.Model):
    module = models.CharField(primary_key=True, max_length=20)
    code = models.CharField(max_length=20)
    branchcode = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    is_html = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    message_transport_type = models.ForeignKey('MessageTransportTypes', models.DO_NOTHING, db_column='message_transport_type')
    lang = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'letter'
        unique_together = (('module', 'code', 'branchcode', 'message_transport_type', 'lang'),)


class LibraryGroups(models.Model):
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    title = models.CharField(unique=True, max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ft_hide_patron_info = models.IntegerField()
    ft_search_groups_opac = models.IntegerField()
    ft_search_groups_staff = models.IntegerField()
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'library_groups'


class Linktracker(models.Model):
    biblionumber = models.IntegerField(blank=True, null=True)
    itemnumber = models.IntegerField(blank=True, null=True)
    borrowernumber = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    timeclicked = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linktracker'


class Localization(models.Model):
    localization_id = models.AutoField(primary_key=True)
    entity = models.CharField(max_length=16)
    code = models.CharField(max_length=64)
    lang = models.CharField(max_length=25)
    translation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localization'
        unique_together = (('entity', 'code', 'lang'),)


class MarcMatchers(models.Model):
    matcher_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    record_type = models.CharField(max_length=10)
    threshold = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'marc_matchers'


class MarcModificationTemplateActions(models.Model):
    mmta_id = models.AutoField(primary_key=True)
    template = models.ForeignKey('MarcModificationTemplates', models.DO_NOTHING)
    ordering = models.IntegerField()
    action = models.CharField(max_length=22)
    field_number = models.SmallIntegerField()
    from_field = models.CharField(max_length=3)
    from_subfield = models.CharField(max_length=1, blank=True, null=True)
    field_value = models.CharField(max_length=100, blank=True, null=True)
    to_field = models.CharField(max_length=3, blank=True, null=True)
    to_subfield = models.CharField(max_length=1, blank=True, null=True)
    to_regex_search = models.TextField(blank=True, null=True)
    to_regex_replace = models.TextField(blank=True, null=True)
    to_regex_modifiers = models.CharField(max_length=8, blank=True, null=True)
    conditional = models.CharField(max_length=6, blank=True, null=True)
    conditional_field = models.CharField(max_length=3, blank=True, null=True)
    conditional_subfield = models.CharField(max_length=1, blank=True, null=True)
    conditional_comparison = models.CharField(max_length=10, blank=True, null=True)
    conditional_value = models.TextField(blank=True, null=True)
    conditional_regex = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marc_modification_template_actions'


class MarcModificationTemplates(models.Model):
    template_id = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'marc_modification_templates'


class MarcSubfieldStructure(models.Model):
    tagfield = models.CharField(max_length=3)
    tagsubfield = models.CharField(max_length=1)
    liblibrarian = models.CharField(max_length=255)
    libopac = models.CharField(max_length=255)
    repeatable = models.IntegerField()
    mandatory = models.IntegerField()
    kohafield = models.CharField(max_length=40, blank=True, null=True)
    tab = models.IntegerField(blank=True, null=True)
    authorised_value = models.ForeignKey(AuthorisedValueCategories, models.DO_NOTHING, db_column='authorised_value', blank=True, null=True)
    authtypecode = models.CharField(max_length=20, blank=True, null=True)
    value_builder = models.CharField(max_length=80, blank=True, null=True)
    isurl = models.IntegerField(blank=True, null=True)
    hidden = models.IntegerField(blank=True, null=True)
    frameworkcode = models.CharField(primary_key=True, max_length=4)
    seealso = models.CharField(max_length=1100, blank=True, null=True)
    link = models.CharField(max_length=80, blank=True, null=True)
    defaultvalue = models.TextField(blank=True, null=True)
    maxlength = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'marc_subfield_structure'
        unique_together = (('frameworkcode', 'tagfield', 'tagsubfield'),)


class MarcTagStructure(models.Model):
    tagfield = models.CharField(max_length=3)
    liblibrarian = models.CharField(max_length=255)
    libopac = models.CharField(max_length=255)
    repeatable = models.IntegerField()
    mandatory = models.IntegerField()
    authorised_value = models.CharField(max_length=10, blank=True, null=True)
    ind1_defaultvalue = models.CharField(max_length=1)
    ind2_defaultvalue = models.CharField(max_length=1)
    frameworkcode = models.CharField(primary_key=True, max_length=4)

    class Meta:
        managed = False
        db_table = 'marc_tag_structure'
        unique_together = (('frameworkcode', 'tagfield'),)


class Matchchecks(models.Model):
    matcher = models.ForeignKey(MarcMatchers, models.DO_NOTHING)
    matchcheck_id = models.AutoField(primary_key=True)
    source_matchpoint = models.ForeignKey('Matchpoints', models.DO_NOTHING, related_name='matchcheck_source')
    target_matchpoint = models.ForeignKey('Matchpoints', models.DO_NOTHING, related_name='matchcheck_target')

    class Meta:
        managed = False
        db_table = 'matchchecks'


class MatcherMatchpoints(models.Model):
    matcher = models.ForeignKey(MarcMatchers, models.DO_NOTHING)
    matchpoint = models.ForeignKey('Matchpoints', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'matcher_matchpoints'


class MatchpointComponentNorms(models.Model):
    matchpoint_component = models.ForeignKey('MatchpointComponents', models.DO_NOTHING)
    sequence = models.IntegerField()
    norm_routine = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'matchpoint_component_norms'


class MatchpointComponents(models.Model):
    matchpoint = models.ForeignKey('Matchpoints', models.DO_NOTHING)
    matchpoint_component_id = models.AutoField(primary_key=True)
    sequence = models.IntegerField()
    tag = models.CharField(max_length=3)
    subfields = models.CharField(max_length=40)
    offset = models.IntegerField()
    length = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'matchpoint_components'


class Matchpoints(models.Model):
    matcher = models.ForeignKey(MarcMatchers, models.DO_NOTHING)
    matchpoint_id = models.AutoField(primary_key=True)
    search_index = models.CharField(max_length=30)
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'matchpoints'


class MessageAttributes(models.Model):
    message_attribute_id = models.AutoField(primary_key=True)
    message_name = models.CharField(unique=True, max_length=40)
    takes_days = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'message_attributes'


class MessageQueue(models.Model):
    message_id = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    letter_code = models.CharField(max_length=64, blank=True, null=True)
    message_transport_type = models.ForeignKey('MessageTransportTypes', models.DO_NOTHING, db_column='message_transport_type')
    status = models.CharField(max_length=7)
    time_queued = models.DateTimeField()
    to_address = models.TextField(blank=True, null=True)
    from_address = models.TextField(blank=True, null=True)
    content_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_queue'


class MessageTransportTypes(models.Model):
    message_transport_type = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'message_transport_types'


class MessageTransports(models.Model):
    message_attribute = models.OneToOneField(MessageAttributes, models.DO_NOTHING, primary_key=True)
    message_transport_type = models.ForeignKey(MessageTransportTypes, models.DO_NOTHING, db_column='message_transport_type')
    is_digest = models.IntegerField()
    letter_module = models.CharField(max_length=20)
    letter_code = models.CharField(max_length=20)
    branchcode = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'message_transports'
        unique_together = (('message_attribute', 'message_transport_type', 'is_digest'),)


class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    borrowernumber = models.IntegerField()
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    message_type = models.CharField(max_length=1)
    message = models.TextField()
    message_date = models.DateTimeField()
    manager = models.ForeignKey(Borrowers, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messages'


class MiscFiles(models.Model):
    file_id = models.AutoField(primary_key=True)
    table_tag = models.CharField(max_length=255)
    record_id = models.IntegerField()
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    file_description = models.CharField(max_length=255, blank=True, null=True)
    file_content = models.TextField()
    date_uploaded = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'misc_files'


class NeedMergeAuthorities(models.Model):
    authid = models.BigIntegerField()
    authid_new = models.BigIntegerField(blank=True, null=True)
    reportxml = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    done = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'need_merge_authorities'


class OaiSets(models.Model):
    spec = models.CharField(unique=True, max_length=80)
    name = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'oai_sets'


class OaiSetsBiblios(models.Model):
    biblionumber = models.IntegerField(primary_key=True)
    set = models.ForeignKey(OaiSets, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'oai_sets_biblios'
        unique_together = (('biblionumber', 'set'),)


class OaiSetsDescriptions(models.Model):
    set = models.ForeignKey(OaiSets, models.DO_NOTHING)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'oai_sets_descriptions'


class OaiSetsMappings(models.Model):
    set = models.ForeignKey(OaiSets, models.DO_NOTHING)
    marcfield = models.CharField(max_length=3)
    marcsubfield = models.CharField(max_length=1)
    operator = models.CharField(max_length=8)
    marcvalue = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'oai_sets_mappings'


class OauthAccessTokens(models.Model):
    access_token = models.CharField(primary_key=True, max_length=191)
    client_id = models.CharField(max_length=191)
    expires = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oauth_access_tokens'


class OldIssues(models.Model):
    issue_id = models.IntegerField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    itemnumber = models.ForeignKey(Items, models.DO_NOTHING, db_column='itemnumber', blank=True, null=True)
    date_due = models.DateTimeField(blank=True, null=True)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    returndate = models.DateTimeField(blank=True, null=True)
    lastreneweddate = models.DateTimeField(blank=True, null=True)
    renewals = models.IntegerField(blank=True, null=True)
    auto_renew = models.IntegerField(blank=True, null=True)
    auto_renew_error = models.CharField(max_length=32, blank=True, null=True)
    timestamp = models.DateTimeField()
    issuedate = models.DateTimeField(blank=True, null=True)
    onsite_checkout = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    notedate = models.DateTimeField(blank=True, null=True)
    noteseen = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'old_issues'


class OldReserves(models.Model):
    reserve_id = models.IntegerField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    reservedate = models.DateField(blank=True, null=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber', blank=True, null=True)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    notificationdate = models.DateField(blank=True, null=True)
    reminderdate = models.DateField(blank=True, null=True)
    cancellationdate = models.DateField(blank=True, null=True)
    reservenotes = models.TextField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    found = models.CharField(max_length=1, blank=True, null=True)
    timestamp = models.DateTimeField()
    itemnumber = models.ForeignKey(Items, models.DO_NOTHING, db_column='itemnumber', blank=True, null=True)
    waitingdate = models.DateField(blank=True, null=True)
    expirationdate = models.DateField(blank=True, null=True)
    lowestpriority = models.IntegerField(db_column='lowestPriority')  # Field name made lowercase.
    suspend = models.IntegerField()
    suspend_until = models.DateTimeField(blank=True, null=True)
    itemtype = models.ForeignKey(Itemtypes, models.DO_NOTHING, db_column='itemtype', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'old_reserves'


class OpacNews(models.Model):
    idnew = models.AutoField(primary_key=True)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    lang = models.CharField(max_length=25)
    timestamp = models.DateTimeField()
    expirationdate = models.DateField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opac_news'


class Overduerules(models.Model):
    overduerules_id = models.AutoField(primary_key=True)
    branchcode = models.CharField(max_length=10)
    categorycode = models.CharField(max_length=10)
    delay1 = models.IntegerField(blank=True, null=True)
    letter1 = models.CharField(max_length=20, blank=True, null=True)
    debarred1 = models.CharField(max_length=1, blank=True, null=True)
    delay2 = models.IntegerField(blank=True, null=True)
    debarred2 = models.CharField(max_length=1, blank=True, null=True)
    letter2 = models.CharField(max_length=20, blank=True, null=True)
    delay3 = models.IntegerField(blank=True, null=True)
    letter3 = models.CharField(max_length=20, blank=True, null=True)
    debarred3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'overduerules'
        unique_together = (('branchcode', 'categorycode'),)


class OverduerulesTransportTypes(models.Model):
    letternumber = models.IntegerField()
    message_transport_type = models.ForeignKey(MessageTransportTypes, models.DO_NOTHING, db_column='message_transport_type')
    overduerules = models.ForeignKey(Overduerules, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'overduerules_transport_types'


class PatronConsent(models.Model):
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')
    type = models.CharField(max_length=15, blank=True, null=True)
    given_on = models.DateTimeField(blank=True, null=True)
    refused_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patron_consent'


class PatronListPatrons(models.Model):
    patron_list_patron_id = models.AutoField(primary_key=True)
    patron_list = models.ForeignKey('PatronLists', models.DO_NOTHING)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')

    class Meta:
        managed = False
        db_table = 'patron_list_patrons'


class PatronLists(models.Model):
    patron_list_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='owner')
    shared = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patron_lists'


class Patronimage(models.Model):
    borrowernumber = models.OneToOneField(Borrowers, models.DO_NOTHING, db_column='borrowernumber', primary_key=True)
    mimetype = models.CharField(max_length=15)
    imagefile = models.TextField()

    class Meta:
        managed = False
        db_table = 'patronimage'


class PendingOfflineOperations(models.Model):
    operationid = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=30)
    branchcode = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=10)
    barcode = models.CharField(max_length=20, blank=True, null=True)
    cardnumber = models.CharField(max_length=32, blank=True, null=True)
    amount = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pending_offline_operations'


class Permissions(models.Model):
    module_bit = models.OneToOneField('Userflags', models.DO_NOTHING, db_column='module_bit', primary_key=True)
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'
        unique_together = (('module_bit', 'code'),)


class PluginData(models.Model):
    plugin_class = models.CharField(primary_key=True, max_length=255)
    plugin_key = models.CharField(max_length=255)
    plugin_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plugin_data'
        unique_together = (('plugin_class', 'plugin_key'),)


class Printers(models.Model):
    printername = models.CharField(primary_key=True, max_length=40)
    printqueue = models.CharField(max_length=20, blank=True, null=True)
    printtype = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'printers'


class PrintersProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    printer_name = models.CharField(max_length=40)
    template_id = models.IntegerField()
    paper_bin = models.CharField(max_length=20)
    offset_horz = models.FloatField()
    offset_vert = models.FloatField()
    creep_horz = models.FloatField()
    creep_vert = models.FloatField()
    units = models.CharField(max_length=20)
    creator = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'printers_profile'
        unique_together = (('printer_name', 'template_id', 'paper_bin', 'creator'),)


class Quotes(models.Model):
    source = models.TextField(blank=True, null=True)
    text = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'quotes'


class Ratings(models.Model):
    borrowernumber = models.OneToOneField(Borrowers, models.DO_NOTHING, db_column='borrowernumber', primary_key=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    rating_value = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ratings'
        unique_together = (('borrowernumber', 'biblionumber'),)


class RefundLostItemFeeRules(models.Model):
    branchcode = models.CharField(primary_key=True, max_length=10)
    refund = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'refund_lost_item_fee_rules'


class RepeatableHolidays(models.Model):
    branchcode = models.CharField(max_length=10)
    weekday = models.SmallIntegerField(blank=True, null=True)
    day = models.SmallIntegerField(blank=True, null=True)
    month = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'repeatable_holidays'


class ReportsDictionary(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)
    saved_sql = models.TextField(blank=True, null=True)
    report_area = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports_dictionary'


class Reserves(models.Model):
    reserve_id = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')
    reservedate = models.DateField(blank=True, null=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING, db_column='branchcode', blank=True, null=True)
    notificationdate = models.DateField(blank=True, null=True)
    reminderdate = models.DateField(blank=True, null=True)
    cancellationdate = models.DateField(blank=True, null=True)
    reservenotes = models.TextField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    found = models.CharField(max_length=1, blank=True, null=True)
    timestamp = models.DateTimeField()
    itemnumber = models.ForeignKey(Items, models.DO_NOTHING, db_column='itemnumber', related_name='reserves_set', blank=True, null=True)
    waitingdate = models.DateField(blank=True, null=True)
    expirationdate = models.DateField(blank=True, null=True)
    lowestpriority = models.IntegerField(db_column='lowestPriority')  # Field name made lowercase.
    suspend = models.IntegerField()
    suspend_until = models.DateTimeField(blank=True, null=True)
    itemtype = models.ForeignKey(Itemtypes, models.DO_NOTHING, db_column='itemtype', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reserves'


class Reviews(models.Model):
    reviewid = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True) # The borrower that left this comment
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber', blank=True, null=True) # The biblio record for which this comment is.
    review = models.TextField(blank=True, null=True) #the body of the comment
    approved = models.IntegerField(blank=True, null=True) #whether this comment has been approved by a librarian (1 for yes, 0 for no)
    datereviewed = models.DateTimeField(blank=True, null=True) #the date the comment was left

    class Meta:
        managed = False
        db_table = 'reviews'


class SavedReports(models.Model):
    report_id = models.IntegerField(blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    date_run = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saved_reports'


class SavedSql(models.Model):
    borrowernumber = models.IntegerField(blank=True, null=True) # The staff member who created this report
    date_created = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    savedsql = models.TextField(blank=True, null=True)
    last_run = models.DateTimeField(blank=True, null=True)
    report_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cache_expiry = models.IntegerField()
    public = models.IntegerField()
    report_area = models.CharField(max_length=6, blank=True, null=True)
    report_group = models.CharField(max_length=80, blank=True, null=True)
    report_subgroup = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saved_sql'


class SearchField(models.Model):
    name = models.CharField(unique=True, max_length=255)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=7)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_field'


class SearchHistory(models.Model):
    userid = models.IntegerField()
    sessionid = models.CharField(max_length=32)
    query_desc = models.CharField(max_length=255)
    query_cgi = models.TextField()
    type = models.CharField(max_length=16)
    total = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'search_history'


class SearchMarcMap(models.Model):
    index_name = models.CharField(max_length=11)
    marc_type = models.CharField(max_length=7)
    marc_field = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'search_marc_map'
        unique_together = (('index_name', 'marc_field', 'marc_type'),)


class SearchMarcToField(models.Model):
    search_marc_map = models.OneToOneField(SearchMarcMap, models.DO_NOTHING, primary_key=True)
    search_field = models.ForeignKey(SearchField, models.DO_NOTHING)
    facet = models.IntegerField(blank=True, null=True)
    suggestible = models.IntegerField(blank=True, null=True)
    sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_marc_to_field'
        unique_together = (('search_marc_map', 'search_field'),)


class Serial(models.Model):
    serialid = models.AutoField(primary_key=True)
    biblionumber = models.CharField(max_length=100)
    subscriptionid = models.CharField(max_length=100)
    serialseq = models.CharField(max_length=100)
    serialseq_x = models.CharField(max_length=100, blank=True, null=True)
    serialseq_y = models.CharField(max_length=100, blank=True, null=True)
    serialseq_z = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField()
    planneddate = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    publisheddate = models.DateField(blank=True, null=True)
    publisheddatetext = models.CharField(max_length=100, blank=True, null=True)
    claimdate = models.DateField(blank=True, null=True)
    claims_count = models.IntegerField(blank=True, null=True)
    routingnotes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serial'


class Serialitems(models.Model):
    itemnumber = models.OneToOneField(Items, models.DO_NOTHING, db_column='itemnumber', primary_key=True)
    serialid = models.ForeignKey(Serial, models.DO_NOTHING, db_column='serialid')

    class Meta:
        managed = False
        db_table = 'serialitems'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    a_session = models.TextField()

    class Meta:
        managed = False
        db_table = 'sessions'


class SmsProviders(models.Model):
    name = models.CharField(unique=True, max_length=255)
    domain = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sms_providers'


class SocialData(models.Model):
    isbn = models.CharField(primary_key=True, max_length=30)
    num_critics = models.IntegerField(blank=True, null=True)
    num_critics_pro = models.IntegerField(blank=True, null=True)
    num_quotations = models.IntegerField(blank=True, null=True)
    num_videos = models.IntegerField(blank=True, null=True)
    score_avg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    num_scores = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'social_data'


class SpecialHolidays(models.Model):
    branchcode = models.CharField(max_length=10)
    day = models.SmallIntegerField()
    month = models.SmallIntegerField()
    year = models.SmallIntegerField()
    isexception = models.SmallIntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'special_holidays'


class Statistics(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    branch = models.CharField(max_length=10, blank=True, null=True)
    proccode = models.CharField(max_length=4, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=16, blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    usercode = models.CharField(max_length=10, blank=True, null=True)
    itemnumber = models.IntegerField(blank=True, null=True)
    itemtype = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=80, blank=True, null=True)
    borrowernumber = models.IntegerField(blank=True, null=True)
    associatedborrower = models.IntegerField(blank=True, null=True)
    ccode = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistics'


class Stockrotationitems(models.Model):
    itemnumber = models.OneToOneField(Items, models.DO_NOTHING, primary_key=True)
    stage = models.ForeignKey('Stockrotationstages', models.DO_NOTHING)
    indemand = models.IntegerField()
    fresh = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stockrotationitems'


class Stockrotationrotas(models.Model):
    rota_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    cyclical = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stockrotationrotas'


class Stockrotationstages(models.Model):
    stage_id = models.AutoField(primary_key=True)
    position = models.IntegerField()
    rota = models.ForeignKey(Stockrotationrotas, models.DO_NOTHING)
    branchcode = models.ForeignKey(Branches, models.DO_NOTHING)
    duration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stockrotationstages'


class Subscription(models.Model):
    biblionumber = models.IntegerField()
    subscriptionid = models.AutoField(primary_key=True)
    librarian = models.CharField(max_length=100, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    aqbooksellerid = models.IntegerField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    aqbudgetid = models.IntegerField(blank=True, null=True)
    weeklength = models.IntegerField(blank=True, null=True)
    monthlength = models.IntegerField(blank=True, null=True)
    numberlength = models.IntegerField(blank=True, null=True)
    periodicity = models.ForeignKey('SubscriptionFrequencies', models.DO_NOTHING, db_column='periodicity', blank=True, null=True)
    countissuesperunit = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100)
    lastvalue1 = models.IntegerField(blank=True, null=True)
    innerloop1 = models.IntegerField(blank=True, null=True)
    lastvalue2 = models.IntegerField(blank=True, null=True)
    innerloop2 = models.IntegerField(blank=True, null=True)
    lastvalue3 = models.IntegerField(blank=True, null=True)
    innerloop3 = models.IntegerField(blank=True, null=True)
    firstacquidate = models.DateField(blank=True, null=True)
    manualhistory = models.IntegerField()
    irregularity = models.TextField(blank=True, null=True)
    skip_serialseq = models.IntegerField()
    letter = models.CharField(max_length=20, blank=True, null=True)
    numberpattern = models.ForeignKey('SubscriptionNumberpatterns', models.DO_NOTHING, db_column='numberpattern', blank=True, null=True)
    locale = models.CharField(max_length=80, blank=True, null=True)
    distributedto = models.TextField(blank=True, null=True)
    internalnotes = models.TextField(blank=True, null=True)
    callnumber = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=80, blank=True, null=True)
    branchcode = models.CharField(max_length=10)
    lastbranch = models.CharField(max_length=10, blank=True, null=True)
    serialsadditems = models.IntegerField()
    staffdisplaycount = models.CharField(max_length=10, blank=True, null=True)
    opacdisplaycount = models.CharField(max_length=10, blank=True, null=True)
    graceperiod = models.IntegerField()
    enddate = models.DateField(blank=True, null=True)
    closed = models.IntegerField()
    reneweddate = models.DateField(blank=True, null=True)
    itemtype = models.CharField(max_length=10, blank=True, null=True)
    previousitemtype = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription'


class SubscriptionFrequencies(models.Model):
    description = models.TextField()
    displayorder = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=5, blank=True, null=True)
    unitsperissue = models.IntegerField()
    issuesperunit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subscription_frequencies'


class SubscriptionNumberpatterns(models.Model):
    label = models.CharField(max_length=255)
    displayorder = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    numberingmethod = models.CharField(max_length=255)
    label1 = models.CharField(max_length=255, blank=True, null=True)
    add1 = models.IntegerField(blank=True, null=True)
    every1 = models.IntegerField(blank=True, null=True)
    whenmorethan1 = models.IntegerField(blank=True, null=True)
    setto1 = models.IntegerField(blank=True, null=True)
    numbering1 = models.CharField(max_length=255, blank=True, null=True)
    label2 = models.CharField(max_length=255, blank=True, null=True)
    add2 = models.IntegerField(blank=True, null=True)
    every2 = models.IntegerField(blank=True, null=True)
    whenmorethan2 = models.IntegerField(blank=True, null=True)
    setto2 = models.IntegerField(blank=True, null=True)
    numbering2 = models.CharField(max_length=255, blank=True, null=True)
    label3 = models.CharField(max_length=255, blank=True, null=True)
    add3 = models.IntegerField(blank=True, null=True)
    every3 = models.IntegerField(blank=True, null=True)
    whenmorethan3 = models.IntegerField(blank=True, null=True)
    setto3 = models.IntegerField(blank=True, null=True)
    numbering3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription_numberpatterns'


class Subscriptionhistory(models.Model):
    biblionumber = models.IntegerField()
    subscriptionid = models.IntegerField(primary_key=True)
    histstartdate = models.DateField(blank=True, null=True)
    histenddate = models.DateField(blank=True, null=True)
    missinglist = models.TextField()
    recievedlist = models.TextField()
    opacnote = models.CharField(max_length=150)
    librariannote = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'subscriptionhistory'


class Subscriptionroutinglist(models.Model):
    routingid = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')
    ranking = models.IntegerField(blank=True, null=True)
    subscriptionid = models.ForeignKey(Subscription, models.DO_NOTHING, db_column='subscriptionid')

    class Meta:
        managed = False
        db_table = 'subscriptionroutinglist'
        unique_together = (('subscriptionid', 'borrowernumber'),)


class Suggestions(models.Model):
    suggestionid = models.AutoField(primary_key=True)
    suggestedby = models.IntegerField()
    suggesteddate = models.DateField()
    managedby = models.IntegerField(blank=True, null=True)
    manageddate = models.DateField(blank=True, null=True)
    acceptedby = models.IntegerField(blank=True, null=True)
    accepteddate = models.DateField(blank=True, null=True)
    rejectedby = models.IntegerField(blank=True, null=True)
    rejecteddate = models.DateField(blank=True, null=True)
    status = models.CharField(db_column='STATUS', max_length=10)  # Field name made lowercase.
    note = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=80, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    copyrightdate = models.SmallIntegerField(blank=True, null=True)
    publishercode = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField()
    volumedesc = models.CharField(max_length=255, blank=True, null=True)
    publicationyear = models.SmallIntegerField(blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=30, blank=True, null=True)
    biblionumber = models.IntegerField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    patronreason = models.TextField(blank=True, null=True)
    budgetid = models.ForeignKey(Aqbudgets, models.DO_NOTHING, db_column='budgetid', blank=True, null=True)
    branchcode = models.CharField(max_length=10, blank=True, null=True)
    collectiontitle = models.TextField(blank=True, null=True)
    itemtype = models.CharField(max_length=30, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)
    total = models.DecimalField(max_digits=28, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suggestions'


class Systempreferences(models.Model):
    variable = models.CharField(primary_key=True, max_length=50)
    value = models.TextField(blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'systempreferences'


class Tags(models.Model):
    entry = models.CharField(primary_key=True, max_length=255)
    weight = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tags'


class TagsAll(models.Model):
    tag_id = models.AutoField(primary_key=True)
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    term = models.CharField(max_length=255)
    language = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tags_all'


class TagsApproval(models.Model):
    term = models.CharField(primary_key=True, max_length=191)
    approved = models.IntegerField()
    date_approved = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='approved_by', blank=True, null=True)
    weight_total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tags_approval'


class TagsIndex(models.Model):
    term = models.OneToOneField(TagsApproval, models.DO_NOTHING, db_column='term', primary_key=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tags_index'
        unique_together = (('term', 'biblionumber'),)


class TmpHoldsqueue(models.Model):
    biblionumber = models.IntegerField(blank=True, null=True)
    itemnumber = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(max_length=20, blank=True, null=True)
    surname = models.TextField()
    firstname = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    borrowernumber = models.IntegerField()
    cardnumber = models.CharField(max_length=32, blank=True, null=True)
    reservedate = models.DateField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    itemcallnumber = models.CharField(max_length=255, blank=True, null=True)
    holdingbranch = models.CharField(max_length=10, blank=True, null=True)
    pickbranch = models.CharField(max_length=10, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    item_level_request = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tmp_holdsqueue'


class TransportCost(models.Model):
    frombranch = models.OneToOneField(Branches, models.DO_NOTHING, db_column='frombranch', related_name='sources_transport_costs', primary_key=True)
    tobranch = models.ForeignKey(Branches, models.DO_NOTHING, db_column='tobranch', related_name='destination_transport_costs')
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    disable_transfer = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'transport_cost'
        unique_together = (('frombranch', 'tobranch'),)


class UploadedFiles(models.Model):
    hashvalue = models.CharField(max_length=40)
    filename = models.TextField()
    dir = models.TextField()
    filesize = models.IntegerField(blank=True, null=True)
    dtcreated = models.DateTimeField()
    uploadcategorycode = models.TextField(blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    permanent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uploaded_files'


class UserPermissions(models.Model):
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber')
    module_bit = models.ForeignKey(Permissions, models.DO_NOTHING, related_name='module_bit_user_permissions', db_column='module_bit')
    code = models.ForeignKey(Permissions, models.DO_NOTHING, db_column='code', related_name='code_user_permissions', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_permissions'


class Userflags(models.Model):
    bit = models.IntegerField(primary_key=True)
    flag = models.CharField(max_length=30, blank=True, null=True)
    flagdesc = models.CharField(max_length=255, blank=True, null=True)
    defaulton = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userflags'


class VendorEdiAccounts(models.Model):
    description = models.TextField()
    host = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=40, blank=True, null=True)
    password = models.CharField(max_length=40, blank=True, null=True)
    last_activity = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(Aqbooksellers, models.DO_NOTHING, blank=True, null=True)
    download_directory = models.TextField(blank=True, null=True)
    upload_directory = models.TextField(blank=True, null=True)
    san = models.CharField(max_length=20, blank=True, null=True)
    id_code_qualifier = models.CharField(max_length=3, blank=True, null=True)
    transport = models.CharField(max_length=6, blank=True, null=True)
    quotes_enabled = models.IntegerField()
    invoices_enabled = models.IntegerField()
    orders_enabled = models.IntegerField()
    responses_enabled = models.IntegerField()
    auto_orders = models.IntegerField()
    shipment_budget = models.ForeignKey(Aqbudgets, models.DO_NOTHING, db_column='shipment_budget', blank=True, null=True)
    plugin = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'vendor_edi_accounts'


class Virtualshelfcontents(models.Model):
    shelfnumber = models.ForeignKey('Virtualshelves', models.DO_NOTHING, db_column='shelfnumber')
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    flags = models.IntegerField(blank=True, null=True)
    dateadded = models.DateTimeField()
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'virtualshelfcontents'


class Virtualshelfshares(models.Model):
    shelfnumber = models.ForeignKey('Virtualshelves', models.DO_NOTHING, db_column='shelfnumber')
    borrowernumber = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='borrowernumber', blank=True, null=True)
    invitekey = models.CharField(max_length=10, blank=True, null=True)
    sharedate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'virtualshelfshares'


class Virtualshelves(models.Model):
    shelfnumber = models.AutoField(primary_key=True)
    shelfname = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Borrowers, models.DO_NOTHING, db_column='owner', blank=True, null=True)
    category = models.CharField(max_length=1, blank=True, null=True)
    sortfield = models.CharField(max_length=16, blank=True, null=True)
    lastmodified = models.DateTimeField()
    created_on = models.DateTimeField()
    allow_change_from_owner = models.IntegerField(blank=True, null=True)
    allow_change_from_others = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'virtualshelves'


class Z3950Servers(models.Model):
    host = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    db = models.CharField(max_length=255, blank=True, null=True)
    userid = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    servername = models.TextField()
    checked = models.SmallIntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    syntax = models.CharField(max_length=80, blank=True, null=True)
    timeout = models.IntegerField()
    servertype = models.CharField(max_length=3)
    encoding = models.TextField(blank=True, null=True)
    recordtype = models.CharField(max_length=9)
    sru_options = models.CharField(max_length=255, blank=True, null=True)
    sru_fields = models.TextField(blank=True, null=True)
    add_xslt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'z3950servers'


class Zebraqueue(models.Model):
    biblio_auth_number = models.BigIntegerField()
    operation = models.CharField(max_length=20)
    server = models.CharField(max_length=20)
    done = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'zebraqueue'


# Total 215 models
class PatronInfo(models.Model):
    '''
    Model storing information of Patrons for reports like NoDueCertificates, and FineReports.
    Not pointing to the original Borrowers table, as that is provided by Koha and any change in koha database would affect the tables created by us.
    '''
    name = models.CharField(max_length=75)
    ic_number = models.CharField(max_length=25) # Stored in the borrowers table by the name of sort1
    division = models.CharField(max_length=50)
    mem_number = models.CharField(max_length=20) # Stored in the borrowers table by the name of cardnumber
    ref_no_date = models.CharField(max_length=50, null=True) # Ref No. / Date
    ndc_ref_number = models.IntegerField(blank=True, unique=True) # A unique number given by us for NDCs
    fine_ref_number = models.IntegerField(blank=True, unique=True) # A unique number given by us for FineReport
    fine = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'patron_info'

    def __str__(self):
        return self.name

class NoDueCertificate(models.Model):
    report_number = models.IntegerField(blank=True)
    date = models.DateField(auto_now=True)
    addressee = models.ForeignKey('Addressee', related_name='ndcs', on_delete=models.SET_NULL, null=True)
    full_ref = models.CharField(max_length = 40, null=True)
    patrons = models.ManyToManyField('PatronInfo', related_name='ndcs')

    def __str__(self):
        return self.full_ref

    def save(self, *args, **kwargs):
        if not self.full_ref:
            self.full_ref = "IGCAR/SIRD/LISS/CM/{year}/NDC/{addressee}/{report_number}".format(
                year=self.date.year,
                addressee=self.addressee.ref_number,
                report_number=self.report_number)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'no_due_certificate'


class Addressee(models.Model):
    code = models.CharField(max_length=15)
    content = models.TextField(max_length=200)
    ref_number = models.IntegerField()

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'addressee'

class FineReport(models.Model):
    report_number = models.IntegerField(blank=True)
    patrons = models.ManyToManyField('PatronInfo', related_name='fine_reports')
    date = models.DateField(auto_now=True)
    addressee = models.ForeignKey('Addressee', related_name='fine_reports', on_delete=models.SET_NULL, null=True)
    full_ref = models.CharField(max_length = 40, null=True)

    def __str__(self):
        return self.full_ref

    def save(self, *args, **kwargs):
        if not self.full_ref:
            self.full_ref = "IGCAR/SIRD/LISS/CM/{year}/FINE/{addressee}/{report_number}".format(
                year=self.date.year,
                addressee=self.addressee.ref_number,
                report_number=self.report_number)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'fine_report'
