--
-- PostgreSQL database dump
--

-- Dumped from database version 10.7
-- Dumped by pg_dump version 10.7

-- Started on 2019-05-03 13:43:08

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2798 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 196 (class 1259 OID 24577)
-- Name: books; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.books (
    date date,
    image "char"[],
    id text,
    title text,
    subtitle text,
    author text,
    category text,
    editor text,
    description text
);


ALTER TABLE public.books OWNER TO postgres;

--
-- TOC entry 2790 (class 0 OID 24577)
-- Dependencies: 196
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.books (date, image, id, title, subtitle, author, category, editor, description) FROM stdin;
\.


-- Completed on 2019-05-03 13:43:08

--
-- PostgreSQL database dump complete
--

