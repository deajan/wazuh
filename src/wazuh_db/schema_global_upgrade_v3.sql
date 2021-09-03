/*
 * SQL Schema for upgrading databases
 * Copyright (C) 2015-2021, Wazuh Inc.
 *
 * September, 2021
 *
 * This program is a free software, you can redistribute it
 * and/or modify it under the terms of GPLv2.
*/

ALTER TABLE agent ADD COLUMN disconnected_time INTEGER DEFAULT 0;
UPDATE agent SET disconnected_time = (CASE WHEN connection_status != 'active' AND connection_status != 'pending'
                                      THEN STRFTIME('%s', 'NOW')
                                      ELSE 0)