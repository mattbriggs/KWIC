CREATE TABLE corpus (
    corpusid TEXT PRIMARY KEY,
    nowords INTEGER,
    docount INTEGER
);
CREATE TABLE document (
    documentid TEXT PRIMARY KEY,
    corpusid TEXT,
    filepath TEXT,
    nowords INTEGER,
    summary TEXT,
    wordbag TEXT,
    centrality REAL,
    facet1 TEXT,
    facet2 TEXT,
    facet3 TEXT,
    FOREIGN KEY (corpusid)
        REFERENCES corpus (corpusid)
);
CREATE TABLE textline (
    lineid TEXT PRIMARY KEY,
    documentid TEXT NOT NULL,
    lineno INTEGER,
    linetext TEXT,
    possent REAL,
    nuesent REAL,
    negsent REAL,
    compsent REAL,
    FOREIGN KEY (documentid)
        REFERENCES document (documentid)
);
CREATE TABLE entity (
    entityname TEXT NOT NULL PRIMARY KEY,
    variants TEXT
);
Create TABLE context (
    contextid TEXT PRIMARY KEY,
    entityname TEXT NOT NULL,
    lineid TEXT NOT NULL,
    FOREIGN KEY (entityname)
        REFERENCES entity (entityname),
    FOREIGN KEY (lineid)
        REFERENCES textline (lineid)
);
Create TABLE similarity (
    simmilarityid TEXT UNIQUE,
    similarity REAL,
    sourceid TEXT,
    targetid TEXT,
    PRIMARY KEY (sourceid, targetid),
    FOREIGN KEY (sourceid)
        REFERENCES document (documentid),
    FOREIGN KEY (targetid)
        REFERENCES document (documentid)
);
CREATE VIEW entity_network_view AS
    SELECT DISTINCT context.entityname, textline.documentid 
    FROM textline JOIN context 
    ON textline.lineid=context.lineid;
CREATE VIEW kwic_view AS
	SELECT context.entityname, textline.documentid, textline.lineno, textline.linetext, textline.possent, textline.nuesent, textline.negsent, textline.compsent 
	FROM context
	JOIN textline
	ON context.lineid=textline.lineid;

