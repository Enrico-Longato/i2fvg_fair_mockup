from django.db import models


# ======================
# HEADQUARTERS (MAIN)
# ======================
class CompanyRegistryHeadquarters(models.Model):
    cf = models.CharField(max_length=32, primary_key=True)
    prov = models.CharField(max_length=16, blank=True)
    reg_imp_n = models.CharField(max_length=64, blank=True)
    rea = models.CharField(max_length=64, blank=True)
    sede_ul = models.CharField(max_length=64, blank=True)
    tipo_impresa = models.CharField(max_length=128, blank=True)

    n_albo_art = models.CharField(max_length=64, blank=True, db_column="n-albo_art")

    denominazione = models.TextField(blank=True)
    indirizzo = models.TextField(blank=True)
    indirizzo_strad = models.TextField(blank=True)
    indirizzo_cap = models.CharField(max_length=32, blank=True)
    comune = models.CharField(max_length=255, blank=True)
    indirizzo_fraz = models.TextField(blank=True)
    indirizzo_altre = models.TextField(blank=True)

    addetti_aaaa = models.CharField(max_length=16, blank=True)
    addetti_indip = models.CharField(max_length=16, blank=True)
    addetti_dip = models.CharField(max_length=16, blank=True)

    piva = models.CharField(max_length=32, blank=True)
    tel = models.CharField(max_length=64, blank=True)

    capitale = models.CharField(max_length=64, blank=True)
    descrizione_attivita = models.TextField(blank=True)
    capitale_valuta = models.CharField(max_length=32, blank=True)
    stato_impresa = models.CharField(max_length=255, blank=True)

    tipo_sedeul_1 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_2 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_3 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_4 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_5 = models.CharField(max_length=128, blank=True)

    imp_sedi_ee = models.CharField(max_length=32, blank=True)
    imp_eefvg = models.CharField(max_length=32, blank=True)
    imp_pmi = models.CharField(max_length=32, blank=True)
    imp_startup = models.CharField(max_length=32, blank=True)
    imp_femmilile = models.CharField(max_length=64, blank=True)
    imp_giovanile = models.CharField(max_length=64, blank=True)
    imp_straniera = models.CharField(max_length=64, blank=True)

    pec = models.TextField(blank=True, db_column="PEC")

    data_fine_aa = models.CharField(max_length=32, blank=True)
    data_cost = models.CharField(max_length=32, blank=True)
    tipo_localizzazione = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "i2fvg_company_registry_headquarters"

    def __str__(self):
        return self.cf


# ======================
# FILTERED
# ======================
class CompanyRegistryFiltered(models.Model):
    cf = models.ForeignKey(
        CompanyRegistryHeadquarters,
        to_field="cf",
        db_column="cf",
        on_delete=models.CASCADE,
    )

    prov = models.CharField(max_length=16, blank=True)
    reg_imp_n = models.CharField(max_length=64, blank=True)
    rea = models.CharField(max_length=64, blank=True)
    sede_ul = models.CharField(max_length=64, blank=True)
    tipo_impresa = models.CharField(max_length=128, blank=True)

    n_albo_art = models.CharField(max_length=64, blank=True, db_column="n-albo_art")

    denominazione = models.TextField(blank=True)
    indirizzo = models.TextField(blank=True)
    indirizzo_strad = models.TextField(blank=True)
    indirizzo_cap = models.CharField(max_length=32, blank=True)
    comune = models.CharField(max_length=255, blank=True)
    indirizzo_fraz = models.TextField(blank=True)
    indirizzo_altre = models.TextField(blank=True)

    addetti_aaaa = models.CharField(max_length=16, blank=True)
    addetti_indip = models.CharField(max_length=16, blank=True)
    addetti_dip = models.CharField(max_length=16, blank=True)

    piva = models.CharField(max_length=32, blank=True)
    tel = models.CharField(max_length=64, blank=True)

    capitale = models.CharField(max_length=64, blank=True)
    descrizione_attivita = models.TextField(blank=True)
    capitale_valuta = models.CharField(max_length=32, blank=True)
    stato_impresa = models.CharField(max_length=255, blank=True)

    tipo_sedeul_1 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_2 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_3 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_4 = models.CharField(max_length=128, blank=True)
    tipo_sedeul_5 = models.CharField(max_length=128, blank=True)

    imp_sedi_ee = models.CharField(max_length=32, blank=True)
    imp_eefvg = models.CharField(max_length=32, blank=True)
    imp_pmi = models.CharField(max_length=32, blank=True)
    imp_startup = models.CharField(max_length=32, blank=True)
    imp_femmilile = models.CharField(max_length=64, blank=True)
    imp_giovanile = models.CharField(max_length=64, blank=True)
    imp_straniera = models.CharField(max_length=64, blank=True)

    pec = models.TextField(blank=True, db_column="PEC")

    data_fine_aa = models.CharField(max_length=32, blank=True)
    data_cost = models.CharField(max_length=32, blank=True)
    tipo_localizzazione = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "i2fvg_company_registry_filtered"


# ======================
# FINANCIAL
# ======================
class Financial(models.Model):
    cf = models.ForeignKey(
        CompanyRegistryHeadquarters,
        to_field="cf",
        db_column="c fiscale",
        on_delete=models.CASCADE,
    )

    cia = models.CharField(max_length=16, blank=True)
    rea = models.CharField(max_length=64, blank=True)
    anno = models.CharField(max_length=16, blank=True)

    totale_attivo = models.CharField(max_length=64, blank=True, db_column="Totale attivo")
    totale_immobilizzazioni_immateriali = models.CharField(max_length=64, blank=True, db_column="Totale Immobilizzazioni immateriali")
    crediti_esigibili_entro_esercizio_successivo = models.CharField(max_length=64, blank=True, db_column="Crediti esigibili entro l'esercizio successivo")
    totale_patrimonio_netto = models.CharField(max_length=64, blank=True, db_column="Totale patrimonio netto")
    debiti_esigibili_entro_esercizio_successivo = models.CharField(max_length=64, blank=True, db_column="Debiti esigibili entro l'esercizio successivo")
    totale_valore_della_produzione = models.CharField(max_length=64, blank=True, db_column="Totale valore della produzione")
    ricavi_delle_vendite = models.CharField(max_length=64, blank=True, db_column="Ricavi delle vendite")
    totale_costi_del_personale = models.CharField(max_length=64, blank=True, db_column="Totale Costi del Personale")
    differenza_tra_valore_e_costi_della_produzione = models.CharField(max_length=64, blank=True, db_column="Differenza tra valore e costi della produzione")
    ammortamento_immobilizzazione_immateriali = models.CharField(max_length=64, blank=True, db_column="Ammortamento Immobilizzazione Immateriali")
    utile_perdita_esercizio_ultimi = models.CharField(max_length=64, blank=True, db_column="Utile/perdita esercizio ultimi")
    valore_aggiunto = models.CharField(max_length=64, blank=True, db_column="valore aggiunto")
    tot_aam_acc_svalutazioni = models.CharField(max_length=64, blank=True, db_column="tot.aam.acc.svalutazioni")
    ron_reddito_operativo_netto = models.CharField(max_length=64, blank=True, db_column="(ron) reddito operativo netto")
    immobilizzazioni_materiali = models.CharField(max_length=64, blank=True, db_column="Immobilizzazioni materiali")
    immobilizzazioni_finanziarie = models.CharField(max_length=64, blank=True, db_column="Immobilizzazioni finanziarie")
    attivo_circolante = models.CharField(max_length=64, blank=True, db_column="Attivo Circolante")

    class Meta:
        db_table = "i2fvg_financial"


# ======================
# PROJECT
# ======================
class Project(models.Model):
    projectID = models.CharField(max_length=32, primary_key=True)

    acronym = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=64, blank=True)
    title = models.TextField(blank=True)

    startDate = models.CharField(max_length=32, blank=True)
    endDate = models.CharField(max_length=32, blank=True)
    totalCost = models.CharField(max_length=64, blank=True)
    ecMaxContribution = models.CharField(max_length=64, blank=True)

    legalBasis = models.CharField(max_length=255, blank=True)
    topics = models.TextField(blank=True)
    ecSignatureDate = models.CharField(max_length=32, blank=True)

    frameworkProgramme = models.CharField(max_length=64, blank=True)
    masterCall = models.CharField(max_length=255, blank=True)
    subCall = models.CharField(max_length=255, blank=True)
    fundingScheme = models.CharField(max_length=128, blank=True)

    objective = models.TextField(blank=True)
    contentUpdateDate = models.CharField(max_length=32, blank=True)
    rcn = models.CharField(max_length=64, blank=True)

    grantDoi = models.CharField(max_length=255, blank=True)
    keywords = models.TextField(blank=True)
    coordinator = models.TextField(blank=True)
    participants = models.TextField(blank=True)

    class Meta:
        db_table = "project"


# ======================
# ORGANIZATION
# ======================
class Organization(models.Model):
    project = models.ForeignKey(
        Project,
        to_field="projectID",
        db_column="projectID",
        on_delete=models.CASCADE,
    )

    cf = models.ForeignKey(
        CompanyRegistryHeadquarters,
        to_field="cf",
        db_column="cf",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    projectAcronym = models.CharField(max_length=255, blank=True)
    organisationID = models.CharField(max_length=32)
    vatNumber = models.CharField(max_length=64, blank=True)
    name = models.TextField(blank=True)
    shortName = models.CharField(max_length=255, blank=True)
    SME = models.CharField(max_length=16, blank=True)
    activityType = models.CharField(max_length=64, blank=True)

    street = models.TextField(blank=True)
    postCode = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=64, blank=True)
    nutsCode = models.CharField(max_length=64, blank=True)
    geolocation = models.CharField(max_length=128, blank=True)

    organizationURL = models.TextField(blank=True)
    contactForm = models.TextField(blank=True)

    contentUpdateDate = models.CharField(max_length=32, blank=True)
    rcn = models.CharField(max_length=64, blank=True)
    order = models.CharField(max_length=32, blank=True)
    role = models.CharField(max_length=64, blank=True)

    ecContribution = models.CharField(max_length=64, blank=True)
    netEcContribution = models.CharField(max_length=64, blank=True)
    totalCost = models.CharField(max_length=64, blank=True)

    endOfParticipation = models.CharField(max_length=16, blank=True)
    active = models.CharField(max_length=16, blank=True)

    class Meta:
        db_table = "organization"


# ======================
# EUROSCIVOC
# ======================
class EuroSciVoc(models.Model):
    project = models.ForeignKey(
        Project,
        to_field="projectID",
        db_column="projectID",
        on_delete=models.CASCADE,
    )

    euroSciVocCode = models.CharField(max_length=128, blank=True)
    euroSciVocPath = models.TextField(blank=True)
    euroSciVocTitle = models.CharField(max_length=255, blank=True)
    euroSciVocDescription = models.TextField(blank=True)
    livello_1 = models.CharField(max_length=255, blank=True)
    livello_2 = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "euroscivoc"
