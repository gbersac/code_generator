package models

import scala.xml.Node

import play.api.libs.json._

import anorm.RowParser
import anorm.SqlParser._
import jto.validation.{From, Path, Rule, ValidationError}
import org.joda.time.DateTime
import org.joda.time.format.DateTimeFormat

import models.Constants.{OMDEStatut, StatutScore}
import services.WriteError
import utils.{Anorm, JtoValidationUtils}

case class Root(
  decaissement: Root.Decaissement,
  reference: Root.Reference,
  tiersClient: Root.TiersClient,
  declencheur: String,
  bien: Root.Bien,
  signaletique: Root.Signaletique,
  canalApport: Root.CanalApport,
  financement: Root.Financement,
  cleContrat: Root.CleContrat,
  suivi: Root.Suivi
)

object Root {
  implicit val fmt = Json.format[Root]

  implicit lazy val xmlRule: Rule[Node, Root] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "decaissement" \ "cleDecaissement").read[Decaissement] ~
      (__ \ "root" \ "reference").read[Reference] ~
      (__ \ "root" \ "tiersClient" \ "cleAdresseTiersPart").read[TiersClient] ~
      (__ \ "root" \ "declencheur" \ "codeDeclencheur").read[String] ~
      (__ \ "root" \ "bien").read[Bien] ~
      (__ \ "root" \ "signaletique").read[Signaletique] ~
      (__ \ "root" \ "canalApport").read[CanalApport] ~
      (__ \ "root" \ "financement").read[Financement] ~
      (__ \ "root" \ "cleContrat").read[CleContrat] ~
      (__ \ "root" \ "suivi").read[Suivi]
    )(Root.apply)
  }
case class Decaissement(
  cleDecaissement: String,
  dateDécaissement: DateTime,
  montantDecaissement: Decaissement.MontantDecaissement,
  tiersFournisseur: Decaissement.TiersFournisseur,
  flagPayee: String
)

object Decaissement {
  implicit val fmt = Json.format[Decaissement]

  implicit lazy val xmlRule: Rule[Node, Decaissement] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "decaissement" \ "cleDecaissement" \ "referenceExterneDecaissement").read[String] ~
      (__ \ "root" \ "decaissement" \ "dateDécaissement").read[DateTime] ~
      (__ \ "root" \ "decaissement" \ "montantDecaissement").read[MontantDecaissement] ~
      (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleAdresseTiersFrs").read[TiersFournisseur] ~
      (__ \ "root" \ "decaissement" \ "flagPayee").read[String]
    )(Decaissement.apply)
  }
  case class MontantDecaissement(
    codeNatureTVA: String,
    tauxTVA: String,
    montantHT: String,
    codeTerritorialite: String
  )
  
  object MontantDecaissement {
    implicit val fmt = Json.format[MontantDecaissement]
  
    implicit lazy val xmlRule: Rule[Node, MontantDecaissement] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "decaissement" \ "montantDecaissement" \ "codeNatureTVA").read[String] ~
        (__ \ "root" \ "decaissement" \ "montantDecaissement" \ "tauxTVA").read[String] ~
        (__ \ "root" \ "decaissement" \ "montantDecaissement" \ "montantHT").read[String] ~
        (__ \ "root" \ "decaissement" \ "montantDecaissement" \ "codeTerritorialite").read[String]
      )(MontantDecaissement.apply)
    }
  
  }

  case class TiersFournisseur(
    cleTiersCALFrs: TiersFournisseur.CleTiersCALFrs,
    cleAdresseTiersFrs: String,
    nomFournisseur: String
  )
  
  object TiersFournisseur {
    implicit val fmt = Json.format[TiersFournisseur]
  
    implicit lazy val xmlRule: Rule[Node, TiersFournisseur] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs").read[CleTiersCALFrs] ~
        (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleAdresseTiersFrs" \ "referenceExterneAdresse").read[String] ~
        (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "nomFournisseur").read[String]
      )(TiersFournisseur.apply)
    }
      case class CleTiersCALFrs(
        siren: String,
        prenom: String,
        nic: String,
        dateNaissance: DateTime,
        referenceExterneTiers: String,
        codeCommuneNaissance: String,
        nomPatronymique: String
      )
      
      object CleTiersCALFrs {
        implicit val fmt = Json.format[CleTiersCALFrs]
      
        implicit lazy val xmlRule: Rule[Node, CleTiersCALFrs] = From[Node] { __ =>
          import jto.validation.xml.Rules._
          implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
      
          (
            (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs" \ "siren").read[String] ~
            (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs" \ "prenom").read[String] ~
            (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs" \ "nic").read[String] ~
            (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs" \ "dateNaissance").read[DateTime] ~
            (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs" \ "referenceExterneTiers").read[String] ~
            (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs" \ "codeCommuneNaissance").read[String] ~
            (__ \ "root" \ "decaissement" \ "tiersFournisseur" \ "cleTiersCALFrs" \ "nomPatronymique").read[String]
          )(CleTiersCALFrs.apply)
        }
      
      }
  }
}

case class Reference(
  prefixe: String,
  unite: String,
  grandeur: String
)

object Reference {
  implicit val fmt = Json.format[Reference]

  implicit lazy val xmlRule: Rule[Node, Reference] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "reference" \ "prefixe").read[String] ~
      (__ \ "root" \ "reference" \ "unite").read[String] ~
      (__ \ "root" \ "reference" \ "grandeur").read[String]
    )(Reference.apply)
  }

}

case class TiersClient(
  cleAdresseTiersPart: String,
  cleTiersCALClient: TiersClient.CleTiersCALClient
)

object TiersClient {
  implicit val fmt = Json.format[TiersClient]

  implicit lazy val xmlRule: Rule[Node, TiersClient] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "tiersClient" \ "cleAdresseTiersPart" \ "referenceExterneAdresse").read[String] ~
      (__ \ "root" \ "tiersClient" \ "cleTiersCALClient").read[CleTiersCALClient]
    )(TiersClient.apply)
  }
  case class CleTiersCALClient(
    siren: String,
    prenom: String,
    nic: String,
    dateNaissance: DateTime,
    referenceExterneTiers: String,
    codeCommuneNaissance: String,
    nomPatronymique: String
  )
  
  object CleTiersCALClient {
    implicit val fmt = Json.format[CleTiersCALClient]
  
    implicit lazy val xmlRule: Rule[Node, CleTiersCALClient] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "tiersClient" \ "cleTiersCALClient" \ "siren").read[String] ~
        (__ \ "root" \ "tiersClient" \ "cleTiersCALClient" \ "prenom").read[String] ~
        (__ \ "root" \ "tiersClient" \ "cleTiersCALClient" \ "nic").read[String] ~
        (__ \ "root" \ "tiersClient" \ "cleTiersCALClient" \ "dateNaissance").read[DateTime] ~
        (__ \ "root" \ "tiersClient" \ "cleTiersCALClient" \ "referenceExterneTiers").read[String] ~
        (__ \ "root" \ "tiersClient" \ "cleTiersCALClient" \ "codeCommuneNaissance").read[String] ~
        (__ \ "root" \ "tiersClient" \ "cleTiersCALClient" \ "nomPatronymique").read[String]
      )(CleTiersCALClient.apply)
    }
  
  }
}

case class Bien(
  codeClassificationFrancaiseProduit: String,
  libelleStatutBien: String,
  montantUnitaireImmo: Bien.MontantUnitaireImmo,
  codeMarqueMateriel: String,
  cleAdresseTiersFournisseur: String,
  numeroSerie: String,
  codeFamilleActif: String,
  flagImmatriculable: String,
  immatriculation: String,
  communeLieuLivraison: String,
  montantUnitaireFrais: Bien.MontantUnitaireFrais,
  designation3: String,
  designation2: String,
  designation1: String,
  codeEtat: String,
  codeStatutBien: String,
  flagUsageProfessionnel: String,
  dureeDelaiReglementFournisseur: String,
  dateStatutBien: DateTime,
  dateLivraison: DateTime,
  annee: String,
  codeCategorieBien: String,
  cleTiersCALFournisseur: Bien.CleTiersCALFournisseur,
  cleBien: String
)

object Bien {
  implicit val fmt = Json.format[Bien]

  implicit lazy val xmlRule: Rule[Node, Bien] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "bien" \ "codeClassificationFrancaiseProduit").read[String] ~
      (__ \ "root" \ "bien" \ "libelleStatutBien").read[String] ~
      (__ \ "root" \ "bien" \ "montantUnitaireImmo").read[MontantUnitaireImmo] ~
      (__ \ "root" \ "bien" \ "codeMarqueMateriel").read[String] ~
      (__ \ "root" \ "bien" \ "cleAdresseTiersFournisseur" \ "referenceExterneAdresse").read[String] ~
      (__ \ "root" \ "bien" \ "numeroSerie").read[String] ~
      (__ \ "root" \ "bien" \ "codeFamilleActif").read[String] ~
      (__ \ "root" \ "bien" \ "flagImmatriculable").read[String] ~
      (__ \ "root" \ "bien" \ "immatriculation").read[String] ~
      (__ \ "root" \ "bien" \ "communeLieuLivraison").read[String] ~
      (__ \ "root" \ "bien" \ "montantUnitaireFrais").read[MontantUnitaireFrais] ~
      (__ \ "root" \ "bien" \ "designation3").read[String] ~
      (__ \ "root" \ "bien" \ "designation2").read[String] ~
      (__ \ "root" \ "bien" \ "designation1").read[String] ~
      (__ \ "root" \ "bien" \ "codeEtat").read[String] ~
      (__ \ "root" \ "bien" \ "codeStatutBien").read[String] ~
      (__ \ "root" \ "bien" \ "flagUsageProfessionnel").read[String] ~
      (__ \ "root" \ "bien" \ "dureeDelaiReglementFournisseur").read[String] ~
      (__ \ "root" \ "bien" \ "dateStatutBien").read[DateTime] ~
      (__ \ "root" \ "bien" \ "dateLivraison").read[DateTime] ~
      (__ \ "root" \ "bien" \ "annee").read[String] ~
      (__ \ "root" \ "bien" \ "codeCategorieBien").read[String] ~
      (__ \ "root" \ "bien" \ "cleTiersCALFournisseur").read[CleTiersCALFournisseur] ~
      (__ \ "root" \ "bien" \ "cleBien" \ "referenceExterneBien").read[String]
    )(Bien.apply)
  }
  case class MontantUnitaireImmo(
    codeNatureTVA: String,
    tauxTVA: String,
    montantHT: String,
    codeTerritorialite: String
  )
  
  object MontantUnitaireImmo {
    implicit val fmt = Json.format[MontantUnitaireImmo]
  
    implicit lazy val xmlRule: Rule[Node, MontantUnitaireImmo] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "bien" \ "montantUnitaireImmo" \ "codeNatureTVA").read[String] ~
        (__ \ "root" \ "bien" \ "montantUnitaireImmo" \ "tauxTVA").read[String] ~
        (__ \ "root" \ "bien" \ "montantUnitaireImmo" \ "montantHT").read[String] ~
        (__ \ "root" \ "bien" \ "montantUnitaireImmo" \ "codeTerritorialite").read[String]
      )(MontantUnitaireImmo.apply)
    }
  
  }

  case class MontantUnitaireFrais(
    codeNatureTVA: String,
    tauxTVA: String,
    montantHT: String,
    codeTerritorialite: String
  )
  
  object MontantUnitaireFrais {
    implicit val fmt = Json.format[MontantUnitaireFrais]
  
    implicit lazy val xmlRule: Rule[Node, MontantUnitaireFrais] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "bien" \ "montantUnitaireFrais" \ "codeNatureTVA").read[String] ~
        (__ \ "root" \ "bien" \ "montantUnitaireFrais" \ "tauxTVA").read[String] ~
        (__ \ "root" \ "bien" \ "montantUnitaireFrais" \ "montantHT").read[String] ~
        (__ \ "root" \ "bien" \ "montantUnitaireFrais" \ "codeTerritorialite").read[String]
      )(MontantUnitaireFrais.apply)
    }
  
  }

  case class CleTiersCALFournisseur(
    siren: String,
    prenom: String,
    nic: String,
    dateNaissance: DateTime,
    referenceExterneTiers: String,
    codeCommuneNaissance: String,
    nomPatronymique: String
  )
  
  object CleTiersCALFournisseur {
    implicit val fmt = Json.format[CleTiersCALFournisseur]
  
    implicit lazy val xmlRule: Rule[Node, CleTiersCALFournisseur] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "bien" \ "cleTiersCALFournisseur" \ "siren").read[String] ~
        (__ \ "root" \ "bien" \ "cleTiersCALFournisseur" \ "prenom").read[String] ~
        (__ \ "root" \ "bien" \ "cleTiersCALFournisseur" \ "nic").read[String] ~
        (__ \ "root" \ "bien" \ "cleTiersCALFournisseur" \ "dateNaissance").read[DateTime] ~
        (__ \ "root" \ "bien" \ "cleTiersCALFournisseur" \ "referenceExterneTiers").read[String] ~
        (__ \ "root" \ "bien" \ "cleTiersCALFournisseur" \ "codeCommuneNaissance").read[String] ~
        (__ \ "root" \ "bien" \ "cleTiersCALFournisseur" \ "nomPatronymique").read[String]
      )(CleTiersCALFournisseur.apply)
    }
  
  }
}

case class Signaletique(
  codeOrigine: String,
  montantFinancement: String,
  referenceExterneSource: String,
  codeStatut: String,
  dateDebut: DateTime,
  dateSignature: DateTime,
  dateFinPrevisionelle: DateTime,
  dateFinReelle: DateTime,
  dateStatut: DateTime,
  libelleStatut: String,
  referenceExterneDossEtude: String,
  referenceExterneElementFinancierOrigine: String
)

object Signaletique {
  implicit val fmt = Json.format[Signaletique]

  implicit lazy val xmlRule: Rule[Node, Signaletique] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "signaletique" \ "codeOrigine").read[String] ~
      (__ \ "root" \ "signaletique" \ "montantFinancement").read[String] ~
      (__ \ "root" \ "signaletique" \ "referenceExterneSource").read[String] ~
      (__ \ "root" \ "signaletique" \ "codeStatut").read[String] ~
      (__ \ "root" \ "signaletique" \ "dateDebut").read[DateTime] ~
      (__ \ "root" \ "signaletique" \ "dateSignature").read[DateTime] ~
      (__ \ "root" \ "signaletique" \ "dateFinPrevisionelle").read[DateTime] ~
      (__ \ "root" \ "signaletique" \ "dateFinReelle").read[DateTime] ~
      (__ \ "root" \ "signaletique" \ "dateStatut").read[DateTime] ~
      (__ \ "root" \ "signaletique" \ "libelleStatut").read[String] ~
      (__ \ "root" \ "signaletique" \ "referenceExterneDossEtude").read[String] ~
      (__ \ "root" \ "signaletique" \ "referenceExterneElementFinancierOrigine").read[String]
    )(Signaletique.apply)
  }

}

case class CanalApport(
  codeCanalApport: String,
  cleTiersCALApporteur: CanalApport.CleTiersCALApporteur,
  cleAdresseTiersApporteur: String,
  codeCanalApportDetaille: String
)

object CanalApport {
  implicit val fmt = Json.format[CanalApport]

  implicit lazy val xmlRule: Rule[Node, CanalApport] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "canalApport" \ "codeCanalApport").read[String] ~
      (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur").read[CleTiersCALApporteur] ~
      (__ \ "root" \ "canalApport" \ "cleAdresseTiersApporteur" \ "referenceExterneAdresse").read[String] ~
      (__ \ "root" \ "canalApport" \ "codeCanalApportDetaille").read[String]
    )(CanalApport.apply)
  }
  case class CleTiersCALApporteur(
    siren: String,
    prenom: String,
    nic: String,
    dateNaissance: DateTime,
    referenceExterneTiers: String,
    codeCommuneNaissance: String,
    nomPatronymique: String
  )
  
  object CleTiersCALApporteur {
    implicit val fmt = Json.format[CleTiersCALApporteur]
  
    implicit lazy val xmlRule: Rule[Node, CleTiersCALApporteur] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur" \ "siren").read[String] ~
        (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur" \ "prenom").read[String] ~
        (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur" \ "nic").read[String] ~
        (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur" \ "dateNaissance").read[DateTime] ~
        (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur" \ "referenceExterneTiers").read[String] ~
        (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur" \ "codeCommuneNaissance").read[String] ~
        (__ \ "root" \ "canalApport" \ "cleTiersCALApporteur" \ "nomPatronymique").read[String]
      )(CleTiersCALApporteur.apply)
    }
  
  }
}

case class Financement(
  numDureeMois: String,
  montantVR: Financement.MontantVR,
  codeTypeReglement: String,
  echeance: Financement.Echeance,
  montantFinancement: Financement.MontantFinancement,
  coefficientVR: String,
  cleTiersCALRibClient: Financement.CleTiersCALRibClient,
  dureeDelaiReglement: String
)

object Financement {
  implicit val fmt = Json.format[Financement]

  implicit lazy val xmlRule: Rule[Node, Financement] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "financement" \ "numDureeMois").read[String] ~
      (__ \ "root" \ "financement" \ "montantVR").read[MontantVR] ~
      (__ \ "root" \ "financement" \ "codeTypeReglement").read[String] ~
      (__ \ "root" \ "financement" \ "echeance").read[Echeance] ~
      (__ \ "root" \ "financement" \ "montantFinancement").read[MontantFinancement] ~
      (__ \ "root" \ "financement" \ "coefficientVR").read[String] ~
      (__ \ "root" \ "financement" \ "cleTiersCALRibClient").read[CleTiersCALRibClient] ~
      (__ \ "root" \ "financement" \ "dureeDelaiReglement").read[String]
    )(Financement.apply)
  }
  case class MontantVR(
    codeNatureTVA: String,
    tauxTVA: String,
    montantHT: String,
    codeTerritorialite: String
  )
  
  object MontantVR {
    implicit val fmt = Json.format[MontantVR]
  
    implicit lazy val xmlRule: Rule[Node, MontantVR] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "financement" \ "montantVR" \ "codeNatureTVA").read[String] ~
        (__ \ "root" \ "financement" \ "montantVR" \ "tauxTVA").read[String] ~
        (__ \ "root" \ "financement" \ "montantVR" \ "montantHT").read[String] ~
        (__ \ "root" \ "financement" \ "montantVR" \ "codeTerritorialite").read[String]
      )(MontantVR.apply)
    }
  
  }

  case class Echeance(
    montantInteret: String,
    codeTermeBareme: String,
    cleEcheance: String,
    dateEcheance: DateTime,
    codePeriodiciteBareme: String,
    dateFin: DateTime,
    montantCRD: String,
    dateDebut: DateTime,
    montantCRB: String
  )
  
  object Echeance {
    implicit val fmt = Json.format[Echeance]
  
    implicit lazy val xmlRule: Rule[Node, Echeance] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "financement" \ "echeance" \ "montantInteret").read[String] ~
        (__ \ "root" \ "financement" \ "echeance" \ "codeTermeBareme").read[String] ~
        (__ \ "root" \ "financement" \ "echeance" \ "cleEcheance" \ "referenceExterneEchéance").read[String] ~
        (__ \ "root" \ "financement" \ "echeance" \ "dateEcheance").read[DateTime] ~
        (__ \ "root" \ "financement" \ "echeance" \ "codePeriodiciteBareme").read[String] ~
        (__ \ "root" \ "financement" \ "echeance" \ "dateFin").read[DateTime] ~
        (__ \ "root" \ "financement" \ "echeance" \ "montantCRD").read[String] ~
        (__ \ "root" \ "financement" \ "echeance" \ "dateDebut").read[DateTime] ~
        (__ \ "root" \ "financement" \ "echeance" \ "montantCRB").read[String]
      )(Echeance.apply)
    }
  
  }

  case class MontantFinancement(
    codeNatureTVA: String,
    tauxTVA: String,
    montantHT: String,
    codeTerritorialite: String
  )
  
  object MontantFinancement {
    implicit val fmt = Json.format[MontantFinancement]
  
    implicit lazy val xmlRule: Rule[Node, MontantFinancement] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "financement" \ "montantFinancement" \ "codeNatureTVA").read[String] ~
        (__ \ "root" \ "financement" \ "montantFinancement" \ "tauxTVA").read[String] ~
        (__ \ "root" \ "financement" \ "montantFinancement" \ "montantHT").read[String] ~
        (__ \ "root" \ "financement" \ "montantFinancement" \ "codeTerritorialite").read[String]
      )(MontantFinancement.apply)
    }
  
  }

  case class CleTiersCALRibClient(
    codePaysDomiciliataire: String,
    bban: String,
    referenceExterneRib: String,
    cleIban: String
  )
  
  object CleTiersCALRibClient {
    implicit val fmt = Json.format[CleTiersCALRibClient]
  
    implicit lazy val xmlRule: Rule[Node, CleTiersCALRibClient] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "financement" \ "cleTiersCALRibClient" \ "codePaysDomiciliataire").read[String] ~
        (__ \ "root" \ "financement" \ "cleTiersCALRibClient" \ "bban").read[String] ~
        (__ \ "root" \ "financement" \ "cleTiersCALRibClient" \ "referenceExterneRib").read[String] ~
        (__ \ "root" \ "financement" \ "cleTiersCALRibClient" \ "cleIban").read[String]
      )(CleTiersCALRibClient.apply)
    }
  
  }
}

case class CleContrat(
  referenceExterneContrat: String,
  codeMetier: String,
  referenceExterneOperation: String,
  systemeGestion: String,
  referenceExterneElement: String,
  codeSocieteJuridique: String
)

object CleContrat {
  implicit val fmt = Json.format[CleContrat]

  implicit lazy val xmlRule: Rule[Node, CleContrat] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "cleContrat" \ "referenceExterneContrat").read[String] ~
      (__ \ "root" \ "cleContrat" \ "codeMetier").read[String] ~
      (__ \ "root" \ "cleContrat" \ "referenceExterneOperation").read[String] ~
      (__ \ "root" \ "cleContrat" \ "systemeGestion").read[String] ~
      (__ \ "root" \ "cleContrat" \ "referenceExterneElement").read[String] ~
      (__ \ "root" \ "cleContrat" \ "codeSocieteJuridique").read[String]
    )(CleContrat.apply)
  }

}

case class Suivi(
  datecodeConformite: DateTime,
  codeIndicateurConformite: String,
  motifNonComplétude: Suivi.MotifNonComplétude,
  codeIndicateurCompletude: String,
  dateCodeCompletude: DateTime,
  motifNonConforme: Suivi.MotifNonConforme
)

object Suivi {
  implicit val fmt = Json.format[Suivi]

  implicit lazy val xmlRule: Rule[Node, Suivi] = From[Node] { __ =>
    import jto.validation.xml.Rules._
    implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)

    (
      (__ \ "root" \ "suivi" \ "datecodeConformite").read[DateTime] ~
      (__ \ "root" \ "suivi" \ "codeIndicateurConformite").read[String] ~
      (__ \ "root" \ "suivi" \ "motifNonComplétude").read[MotifNonComplétude] ~
      (__ \ "root" \ "suivi" \ "codeIndicateurCompletude").read[String] ~
      (__ \ "root" \ "suivi" \ "dateCodeCompletude").read[DateTime] ~
      (__ \ "root" \ "suivi" \ "motifNonConforme").read[MotifNonConforme]
    )(Suivi.apply)
  }
  case class MotifNonComplétude(
    codeNonComplétude: String,
    libelleMotifNonComplétude: String,
    dateReceptionCompletude: DateTime,
    dateConstatNonCompletude: DateTime
  )
  
  object MotifNonComplétude {
    implicit val fmt = Json.format[MotifNonComplétude]
  
    implicit lazy val xmlRule: Rule[Node, MotifNonComplétude] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "suivi" \ "motifNonComplétude" \ "codeNonComplétude").read[String] ~
        (__ \ "root" \ "suivi" \ "motifNonComplétude" \ "libelleMotifNonComplétude").read[String] ~
        (__ \ "root" \ "suivi" \ "motifNonComplétude" \ "dateReceptionCompletude").read[DateTime] ~
        (__ \ "root" \ "suivi" \ "motifNonComplétude" \ "dateConstatNonCompletude").read[DateTime]
      )(MotifNonComplétude.apply)
    }
  
  }

  case class MotifNonConforme(
    dateConstatNonConforme: DateTime,
    codeNonConforme: String,
    libelleMotifNonConforme: String,
    dateReceptionConforme: DateTime
  )
  
  object MotifNonConforme {
    implicit val fmt = Json.format[MotifNonConforme]
  
    implicit lazy val xmlRule: Rule[Node, MotifNonConforme] = From[Node] { __ =>
      import jto.validation.xml.Rules._
      implicit val dateTimeTule = JtoValidationUtils.dateTimeXmlRule(OMDEMessage.dateFormatterOMDE)
  
      (
        (__ \ "root" \ "suivi" \ "motifNonConforme" \ "dateConstatNonConforme").read[DateTime] ~
        (__ \ "root" \ "suivi" \ "motifNonConforme" \ "codeNonConforme").read[String] ~
        (__ \ "root" \ "suivi" \ "motifNonConforme" \ "libelleMotifNonConforme").read[String] ~
        (__ \ "root" \ "suivi" \ "motifNonConforme" \ "dateReceptionConforme").read[DateTime]
      )(MotifNonConforme.apply)
    }
  
  }
}
}
