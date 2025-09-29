# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

DROP TABLE IF EXISTS entrada;
DROP TABLE IF EXISTS calculada;

CREATE TABLE entrada (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    velocidad FLOAT NOT NULL,
    angulo FLOAT NOT NULL
);

CREATE TABLE calculada (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    distancia FLOAT NOT NULL
);
