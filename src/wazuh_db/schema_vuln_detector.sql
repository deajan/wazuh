/*
 * SQL Schema for vulnerability detector module
 * Copyright 2018 Wazuh, Inc. <info@wazuh.com>
 * June 28, 2018.
 * This program is a free software, you can redistribute it
 * and/or modify it under the terms of GPLv2.
 */

BEGIN;


CREATE TABLE IF NOT EXISTS AGENTS2 (
         AGENT_ID INT NOT NULL,
         PACKAGE_NAME TEXT NOT NULL,
         VERSION TEXT NOT NULL,
         ARCH TEXT NOT NULL,
         PRIMARY KEY(AGENT_ID, PACKAGE_NAME, VERSION, ARCH)
);


 CREATE TABLE IF NOT EXISTS METADATA2 (
         OS TEXT PRIMARY KEY NOT NULL,
         PRODUCT_NAME TEXT NOT NULL,
         PRODUCT_VERSION TEXT NOT NULL,
         SCHEMA_VERSION TEXT NOT NULL,
         TIMESTAMP DATE NOT NULL
 );

 CREATE TABLE IF NOT EXISTS VULNERABILITIES_INFO2 (
         ID TEXT NOT NULL,
         TITLE TEXT NOT NULL,
         SEVERITY TEXT,
         PUBLISHED TEXT,
         UPDATED TEXT,
         REFERENCE TEXT NOT NULL,
         OS TEXT NOT NULL,
         RATIONALE TEXT,
         PRIMARY KEY(ID, OS)
 );


CREATE TABLE IF NOT EXISTS VULNERABILITIES2 (
        CVEID TEXT NOT NULL REFERENCES VULNERABILITIES_INFO2(ID),
        OS TEXT NOT NULL REFERENCES VULNERABILITIES_INFO2(V_OS),
        PACKAGE TEXT NOT NULL,
        PENDING BOOLEAN NOT NULL,
        OPERATION TEXT NOT NULL,
        OPERATION_VALUE TEXT
);

CREATE INDEX IF NOT EXISTS IN_PACK ON VULNERABILITIES2 (PACKAGE);

END;
