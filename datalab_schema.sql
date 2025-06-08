-- Schéma des tables de la base datalab.sqlite

CREATE TABLE "data.gouv.fr.2022.clean" (
    "uid" TEXT,
    "id" TEXT,
    "nature" TEXT,
    "acheteur_id" TEXT,
    "acheteur_nom" TEXT,
    "acheteur_siren" TEXT,
    "titulaire_id" TEXT,
    "titulaire_typeIdentifiant" TEXT,
    "titulaire_nom" TEXT,
    "titulaire_siren" TEXT,
    "objet" TEXT,
    "montant" REAL,
    "codeCPV" TEXT,
    "procedure" TEXT,
    "dureeMois" INTEGER,
    "dateNotification" TEXT,
    "datePublicationDonnees" TEXT,
    "formePrix" TEXT,
    "attributionAvance" TEXT,
    "offresRecues" INTEGER,
    "marcheInnovant" TEXT,
    "ccag" TEXT,
    "sousTraitanceDeclaree" TEXT,
    "typeGroupementOperateurs" TEXT,
    "tauxAvance" REAL,
    "origineUE" REAL,
    "origineFrance" REAL,
    "lieuExecution_code" TEXT,
    "lieuExecution_typeCode" TEXT,
    "idAccordCadre" TEXT,
    "sourceOpenData" TEXT,
    PRIMARY KEY(uid, titulaire_id, titulaire_typeIdentifiant)
);

CREATE TABLE "marches" (
    "uid" TEXT,
    "id" TEXT,
    "nature" TEXT,
    "acheteur_id" TEXT,
    "acheteur_nom" TEXT,
    "acheteur_siren" TEXT,
    "titulaire_nom" TEXT,
    "titulaire_siren" TEXT,
    "objet" TEXT,
    "montant" REAL,
    "codeCPV" TEXT,
    "procedure" TEXT,
    "dureeMois" INTEGER,
    "dateNotification" TEXT,
    "datePublicationDonnees" TEXT,
    "formePrix" TEXT,
    "attributionAvance" TEXT,
    "offresRecues" INTEGER,
    "marcheInnovant" TEXT,
    "ccag" TEXT,
    "sousTraitanceDeclaree" TEXT,
    "typeGroupementOperateurs" TEXT,
    "tauxAvance" REAL,
    "origineUE" REAL,
    "origineFrance" REAL,
    "lieuExecution_code" TEXT,
    "lieuExecution_typeCode" TEXT,
    "idAccordCadre" TEXT,
    "sourceOpenData" TEXT,
    PRIMARY KEY(uid)
);

CREATE TABLE "acheteurs" (
    "id" TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE "entreprises" (
    "id" TEXT,
    "typeIdentifiant" TEXT,
    PRIMARY KEY(id, typeIdentifiant)
);

CREATE TABLE "marches_titulaires" (
    "marche_uid" TEXT,
    "titulaire_id" TEXT,
    "titulaire_typeIdentifiant" TEXT,
    PRIMARY KEY("marche_uid", "titulaire_id", "titulaire_typeIdentifiant")
);

