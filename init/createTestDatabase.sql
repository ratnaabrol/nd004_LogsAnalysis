---
--- Creates a test database mirroring the structure of the news database.
--- The table creation code is taken from newsdata.sql, if that changes
--- this code will have to be updated.
---
CREATE DATABASE news_test;

ALTER DATABASE news_test OWNER TO vagrant;

\c news_test
--
-- Name: articles; Type: TABLE; Schema: public; Owner: vagrant; Tablespace:
--

CREATE TABLE articles (
    author integer NOT NULL,
    title text NOT NULL,
    slug text NOT NULL,
    lead text,
    body text,
    "time" timestamp with time zone DEFAULT now(),
    id integer NOT NULL
);


ALTER TABLE articles OWNER TO vagrant;

--
-- Name: articles_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE articles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE articles_id_seq OWNER TO vagrant;

--
-- Name: articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE articles_id_seq OWNED BY articles.id;


--
-- Name: authors; Type: TABLE; Schema: public; Owner: vagrant; Tablespace:
--

CREATE TABLE authors (
    name text NOT NULL,
    bio text,
    id integer NOT NULL
);


ALTER TABLE authors OWNER TO vagrant;


--
-- Name: authors_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE authors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE authors_id_seq OWNER TO vagrant;

--
-- Name: authors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE authors_id_seq OWNED BY authors.id;


--
-- Name: log; Type: TABLE; Schema: public; Owner: vagrant; Tablespace:
--

CREATE TABLE log (
    path text,
    ip inet,
    method text,
    status text,
    "time" timestamp with time zone DEFAULT now(),
    id integer NOT NULL
);


ALTER TABLE log OWNER TO vagrant;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE log_id_seq OWNER TO vagrant;


--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE log_id_seq OWNED BY log.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY articles ALTER COLUMN id SET DEFAULT nextval('articles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY authors ALTER COLUMN id SET DEFAULT nextval('authors_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY log ALTER COLUMN id SET DEFAULT nextval('log_id_seq'::regclass);
