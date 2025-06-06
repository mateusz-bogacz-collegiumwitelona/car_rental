--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.2

-- Started on 2025-04-17 12:50:05

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 252 (class 1255 OID 16385)
-- Name: audyt_miasta(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.audyt_miasta() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    uzytkownik_record RECORD;
BEGIN
    IF (TG_OP = 'DELETE') THEN
        -- Dla każdego użytkownika powiązanego z tym miastem, zapisz kompletny rekord historii
        FOR uzytkownik_record IN (SELECT * FROM uzytkownicy WHERE id_zamieszkania = OLD.id_zamieszkania) LOOP
            INSERT INTO historia_zmian (
                tabela_zrodlowa, id_rekordu, operacja, 
                miasto, ulica, nr_ulicy, kod_pocztowy,
                id_user, imie, nazwisko, pesel, email, id_zamieszkania
            ) VALUES (
                'miasta', OLD.id_zamieszkania, 'DELETE',
                OLD.miasto, OLD.ulica, OLD.nr_ulicy, OLD.kod_pocztowy,
                uzytkownik_record.id_user, uzytkownik_record.imie, uzytkownik_record.nazwisko, 
                uzytkownik_record."PESEL", uzytkownik_record.email, uzytkownik_record.id_zamieszkania
            );
        END LOOP;
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        -- Dla każdego użytkownika powiązanego z tym miastem, zapisz kompletny rekord historii
        FOR uzytkownik_record IN (SELECT * FROM uzytkownicy WHERE id_zamieszkania = NEW.id_zamieszkania) LOOP
            INSERT INTO historia_zmian (
                tabela_zrodlowa, id_rekordu, operacja, 
                miasto, ulica, nr_ulicy, kod_pocztowy,
                id_user, imie, nazwisko, pesel, email, id_zamieszkania
            ) VALUES (
                'miasta', NEW.id_zamieszkania, 'UPDATE',
                NEW.miasto, NEW.ulica, NEW.nr_ulicy, NEW.kod_pocztowy,
                uzytkownik_record.id_user, uzytkownik_record.imie, uzytkownik_record.nazwisko, 
                uzytkownik_record."PESEL", uzytkownik_record.email, uzytkownik_record.id_zamieszkania
            );
        END LOOP;
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        -- Dla nowo dodanego miasta, możemy nie mieć jeszcze powiązanych użytkowników
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja, 
            miasto, ulica, nr_ulicy, kod_pocztowy
        ) VALUES (
            'miasta', NEW.id_zamieszkania, 'INSERT',
            NEW.miasto, NEW.ulica, NEW.nr_ulicy, NEW.kod_pocztowy
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.audyt_miasta() OWNER TO admin;

--
-- TOC entry 253 (class 1255 OID 16386)
-- Name: audyt_uzytkownicy(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.audyt_uzytkownicy() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    miasto_record RECORD;
BEGIN
    IF (TG_OP = 'DELETE') THEN
        -- Pobierz dane miasta i zapisz kompletny rekord
        SELECT * INTO miasto_record FROM miasta WHERE id_zamieszkania = OLD.id_zamieszkania;
        
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja,
            miasto, ulica, nr_ulicy, kod_pocztowy,
            id_user, imie, nazwisko, pesel, email, id_zamieszkania
        ) VALUES (
            'uzytkownicy', OLD.id_user, 'DELETE',
            miasto_record.miasto, miasto_record.ulica, miasto_record.nr_ulicy, miasto_record.kod_pocztowy,
            OLD.id_user, OLD.imie, OLD.nazwisko, OLD."PESEL", OLD.email, OLD.id_zamieszkania
        );
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        -- Pobierz dane miasta i zapisz kompletny rekord
        SELECT * INTO miasto_record FROM miasta WHERE id_zamieszkania = NEW.id_zamieszkania;
        
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja,
            miasto, ulica, nr_ulicy, kod_pocztowy,
            id_user, imie, nazwisko, pesel, email, id_zamieszkania
        ) VALUES (
            'uzytkownicy', NEW.id_user, 'UPDATE',
            miasto_record.miasto, miasto_record.ulica, miasto_record.nr_ulicy, miasto_record.kod_pocztowy,
            NEW.id_user, NEW.imie, NEW.nazwisko, NEW."PESEL", NEW.email, NEW.id_zamieszkania
        );
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        -- Pobierz dane miasta i zapisz kompletny rekord
        SELECT * INTO miasto_record FROM miasta WHERE id_zamieszkania = NEW.id_zamieszkania;
        
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja,
            miasto, ulica, nr_ulicy, kod_pocztowy,
            id_user, imie, nazwisko, pesel, email, id_zamieszkania
        ) VALUES (
            'uzytkownicy', NEW.id_user, 'INSERT',
            miasto_record.miasto, miasto_record.ulica, miasto_record.nr_ulicy, miasto_record.kod_pocztowy,
            NEW.id_user, NEW.imie, NEW.nazwisko, NEW."PESEL", NEW.email, NEW.id_zamieszkania
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.audyt_uzytkownicy() OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16387)
-- Name: admin; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.admin (
    id_admin integer NOT NULL,
    imie character varying(50) DEFAULT 'anonymous'::character varying NOT NULL,
    nazwisko character varying(50) DEFAULT 'unknown'::character varying NOT NULL,
    email character varying(50) DEFAULT 'example@example.com'::character varying NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.admin OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16393)
-- Name: admin_id_admin_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.admin_id_admin_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admin_id_admin_seq OWNER TO admin;

--
-- TOC entry 3553 (class 0 OID 0)
-- Dependencies: 218
-- Name: admin_id_admin_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.admin_id_admin_seq OWNED BY public.admin.id_admin;


--
-- TOC entry 219 (class 1259 OID 16394)
-- Name: auta; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auta (
    id_auta integer NOT NULL,
    marka character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    model character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    rocznik integer NOT NULL,
    opis character varying(1000),
    osiagi character varying(1000)
);


ALTER TABLE public.auta OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 16401)
-- Name: auta_id_auta_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auta_id_auta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auta_id_auta_seq OWNER TO admin;

--
-- TOC entry 3554 (class 0 OID 0)
-- Dependencies: 220
-- Name: auta_id_auta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auta_id_auta_seq OWNED BY public.auta.id_auta;


--
-- TOC entry 221 (class 1259 OID 16402)
-- Name: auta_zdj; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auta_zdj (
    id_zdj integer NOT NULL,
    id_auta integer NOT NULL,
    zdj character varying(255) NOT NULL,
    kolejnosc integer DEFAULT 1,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.auta_zdj OWNER TO admin;

--
-- TOC entry 222 (class 1259 OID 16407)
-- Name: auta_zdj_id_zdj_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auta_zdj_id_zdj_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auta_zdj_id_zdj_seq OWNER TO admin;

--
-- TOC entry 3555 (class 0 OID 0)
-- Dependencies: 222
-- Name: auta_zdj_id_zdj_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auta_zdj_id_zdj_seq OWNED BY public.auta_zdj.id_zdj;


--
-- TOC entry 223 (class 1259 OID 16408)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- TOC entry 224 (class 1259 OID 16411)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 16412)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- TOC entry 226 (class 1259 OID 16415)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 16416)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- TOC entry 228 (class 1259 OID 16419)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 229 (class 1259 OID 16420)
-- Name: auth_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO admin;

--
-- TOC entry 230 (class 1259 OID 16425)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- TOC entry 231 (class 1259 OID 16428)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 232 (class 1259 OID 16429)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 233 (class 1259 OID 16430)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- TOC entry 234 (class 1259 OID 16433)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 235 (class 1259 OID 16434)
-- Name: czarna_lista; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.czarna_lista (
    id_bl integer NOT NULL,
    id_user integer NOT NULL,
    powod character varying(50) DEFAULT 'unknown'::character varying NOT NULL,
    data_poczatkowa date NOT NULL,
    data_koncowa date NOT NULL,
    id_admin integer NOT NULL
);


ALTER TABLE public.czarna_lista OWNER TO admin;

--
-- TOC entry 236 (class 1259 OID 16438)
-- Name: czarna_lista_id_bl_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.czarna_lista_id_bl_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.czarna_lista_id_bl_seq OWNER TO admin;

--
-- TOC entry 3556 (class 0 OID 0)
-- Dependencies: 236
-- Name: czarna_lista_id_bl_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.czarna_lista_id_bl_seq OWNED BY public.czarna_lista.id_bl;


--
-- TOC entry 237 (class 1259 OID 16439)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- TOC entry 238 (class 1259 OID 16445)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 239 (class 1259 OID 16446)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- TOC entry 240 (class 1259 OID 16449)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 241 (class 1259 OID 16450)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- TOC entry 242 (class 1259 OID 16455)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 243 (class 1259 OID 16456)
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- TOC entry 244 (class 1259 OID 16461)
-- Name: historia_zmian; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.historia_zmian (
    id_historii integer NOT NULL,
    tabela_zrodlowa character varying(50) NOT NULL,
    id_rekordu integer NOT NULL,
    operacja character varying(10) NOT NULL,
    data_operacji timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    miasto character varying(100),
    ulica character varying(100),
    nr_ulicy character varying(5),
    kod_pocztowy character varying(6),
    id_user integer,
    imie character varying(100),
    nazwisko character varying(100),
    pesel character(11),
    email character varying(50),
    id_zamieszkania integer
);


ALTER TABLE public.historia_zmian OWNER TO admin;

--
-- TOC entry 245 (class 1259 OID 16467)
-- Name: historia_zmian_id_historii_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.historia_zmian_id_historii_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.historia_zmian_id_historii_seq OWNER TO admin;

--
-- TOC entry 3557 (class 0 OID 0)
-- Dependencies: 245
-- Name: historia_zmian_id_historii_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.historia_zmian_id_historii_seq OWNED BY public.historia_zmian.id_historii;


--
-- TOC entry 246 (class 1259 OID 16468)
-- Name: miasta; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.miasta (
    id_zamieszkania integer NOT NULL,
    miasto character varying(100) DEFAULT 'city_name'::character varying NOT NULL,
    ulica character varying(100) DEFAULT 'ulica'::character varying NOT NULL,
    nr_ulicy character varying(5) DEFAULT '1b'::character varying NOT NULL,
    kod_pocztowy character varying(6) DEFAULT '12-345'::character varying NOT NULL
);


ALTER TABLE public.miasta OWNER TO admin;

--
-- TOC entry 247 (class 1259 OID 16475)
-- Name: miasta_id_zamieszkania_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.miasta_id_zamieszkania_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.miasta_id_zamieszkania_seq OWNER TO admin;

--
-- TOC entry 3558 (class 0 OID 0)
-- Dependencies: 247
-- Name: miasta_id_zamieszkania_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.miasta_id_zamieszkania_seq OWNED BY public.miasta.id_zamieszkania;


--
-- TOC entry 248 (class 1259 OID 16476)
-- Name: uzytkownicy; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.uzytkownicy (
    id_user integer NOT NULL,
    imie character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    nazwisko character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    "PESEL" character(11) DEFAULT '00000000000'::bpchar NOT NULL,
    email character varying(50) DEFAULT 'example@example.com'::character varying NOT NULL,
    haslo character varying(100) NOT NULL,
    id_zamieszkania integer NOT NULL
);


ALTER TABLE public.uzytkownicy OWNER TO admin;

--
-- TOC entry 249 (class 1259 OID 16483)
-- Name: uzytkownicy_id_user_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.uzytkownicy_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.uzytkownicy_id_user_seq OWNER TO admin;

--
-- TOC entry 3559 (class 0 OID 0)
-- Dependencies: 249
-- Name: uzytkownicy_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.uzytkownicy_id_user_seq OWNED BY public.uzytkownicy.id_user;


--
-- TOC entry 250 (class 1259 OID 16484)
-- Name: wypozyczenie; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.wypozyczenie (
    id_wypozyczenia integer NOT NULL,
    data_poczatkowa date NOT NULL,
    data_koncowa date NOT NULL,
    id_auta integer NOT NULL,
    id_user integer NOT NULL
);


ALTER TABLE public.wypozyczenie OWNER TO admin;

--
-- TOC entry 251 (class 1259 OID 16487)
-- Name: wypozyczenie_id_wypozyczenia_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.wypozyczenie_id_wypozyczenia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.wypozyczenie_id_wypozyczenia_seq OWNER TO admin;

--
-- TOC entry 3560 (class 0 OID 0)
-- Dependencies: 251
-- Name: wypozyczenie_id_wypozyczenia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.wypozyczenie_id_wypozyczenia_seq OWNED BY public.wypozyczenie.id_wypozyczenia;


--
-- TOC entry 3296 (class 2604 OID 16488)
-- Name: admin id_admin; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.admin ALTER COLUMN id_admin SET DEFAULT nextval('public.admin_id_admin_seq'::regclass);


--
-- TOC entry 3300 (class 2604 OID 16489)
-- Name: auta id_auta; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auta ALTER COLUMN id_auta SET DEFAULT nextval('public.auta_id_auta_seq'::regclass);


--
-- TOC entry 3303 (class 2604 OID 16490)
-- Name: auta_zdj id_zdj; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auta_zdj ALTER COLUMN id_zdj SET DEFAULT nextval('public.auta_zdj_id_zdj_seq'::regclass);


--
-- TOC entry 3306 (class 2604 OID 16491)
-- Name: czarna_lista id_bl; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.czarna_lista ALTER COLUMN id_bl SET DEFAULT nextval('public.czarna_lista_id_bl_seq'::regclass);


--
-- TOC entry 3308 (class 2604 OID 16492)
-- Name: historia_zmian id_historii; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.historia_zmian ALTER COLUMN id_historii SET DEFAULT nextval('public.historia_zmian_id_historii_seq'::regclass);


--
-- TOC entry 3310 (class 2604 OID 16493)
-- Name: miasta id_zamieszkania; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.miasta ALTER COLUMN id_zamieszkania SET DEFAULT nextval('public.miasta_id_zamieszkania_seq'::regclass);


--
-- TOC entry 3315 (class 2604 OID 16494)
-- Name: uzytkownicy id_user; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.uzytkownicy ALTER COLUMN id_user SET DEFAULT nextval('public.uzytkownicy_id_user_seq'::regclass);


--
-- TOC entry 3320 (class 2604 OID 16495)
-- Name: wypozyczenie id_wypozyczenia; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.wypozyczenie ALTER COLUMN id_wypozyczenia SET DEFAULT nextval('public.wypozyczenie_id_wypozyczenia_seq'::regclass);


--
-- TOC entry 3323 (class 2606 OID 16497)
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id_admin);


--
-- TOC entry 3325 (class 2606 OID 16499)
-- Name: auta auta_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auta
    ADD CONSTRAINT auta_pkey PRIMARY KEY (id_auta);


--
-- TOC entry 3327 (class 2606 OID 16501)
-- Name: auta_zdj auta_zdj_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auta_zdj
    ADD CONSTRAINT auta_zdj_pkey PRIMARY KEY (id_zdj);


--
-- TOC entry 3331 (class 2606 OID 16503)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 3336 (class 2606 OID 16505)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 3339 (class 2606 OID 16507)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3333 (class 2606 OID 16509)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 3342 (class 2606 OID 16511)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 3344 (class 2606 OID 16513)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 3352 (class 2606 OID 16515)
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3355 (class 2606 OID 16517)
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- TOC entry 3346 (class 2606 OID 16519)
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3358 (class 2606 OID 16521)
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3361 (class 2606 OID 16523)
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- TOC entry 3349 (class 2606 OID 16525)
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 3363 (class 2606 OID 16527)
-- Name: czarna_lista czarna_lista_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.czarna_lista
    ADD CONSTRAINT czarna_lista_pkey PRIMARY KEY (id_bl);


--
-- TOC entry 3366 (class 2606 OID 16529)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3369 (class 2606 OID 16531)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 3371 (class 2606 OID 16533)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3373 (class 2606 OID 16535)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3376 (class 2606 OID 16537)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 3379 (class 2606 OID 16539)
-- Name: historia_zmian historia_zmian_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.historia_zmian
    ADD CONSTRAINT historia_zmian_pkey PRIMARY KEY (id_historii);


--
-- TOC entry 3381 (class 2606 OID 16541)
-- Name: miasta miasta_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.miasta
    ADD CONSTRAINT miasta_pkey PRIMARY KEY (id_zamieszkania);


--
-- TOC entry 3383 (class 2606 OID 16543)
-- Name: uzytkownicy uzytkownicy_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.uzytkownicy
    ADD CONSTRAINT uzytkownicy_pkey PRIMARY KEY (id_user);


--
-- TOC entry 3385 (class 2606 OID 16545)
-- Name: wypozyczenie wypozyczenie_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.wypozyczenie
    ADD CONSTRAINT wypozyczenie_pkey PRIMARY KEY (id_wypozyczenia);


--
-- TOC entry 3329 (class 1259 OID 16546)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 3334 (class 1259 OID 16547)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 3337 (class 1259 OID 16548)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 3340 (class 1259 OID 16549)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 3350 (class 1259 OID 16550)
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- TOC entry 3353 (class 1259 OID 16551)
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- TOC entry 3356 (class 1259 OID 16552)
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 3359 (class 1259 OID 16553)
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 3347 (class 1259 OID 16554)
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 3364 (class 1259 OID 16555)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 3367 (class 1259 OID 16556)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 3374 (class 1259 OID 16557)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 3377 (class 1259 OID 16558)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 3328 (class 1259 OID 16559)
-- Name: idx_auto_zdjecia_id_auta; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_auto_zdjecia_id_auta ON public.auta_zdj USING btree (id_auta);


--
-- TOC entry 3401 (class 2620 OID 16560)
-- Name: miasta trigger_miasta_audyt; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER trigger_miasta_audyt AFTER INSERT OR DELETE OR UPDATE ON public.miasta FOR EACH ROW EXECUTE FUNCTION public.audyt_miasta();


--
-- TOC entry 3402 (class 2620 OID 16561)
-- Name: uzytkownicy trigger_uzytkownicy_audyt; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER trigger_uzytkownicy_audyt AFTER INSERT OR DELETE OR UPDATE ON public.uzytkownicy FOR EACH ROW EXECUTE FUNCTION public.audyt_uzytkownicy();


--
-- TOC entry 3386 (class 2606 OID 16562)
-- Name: auta_zdj auta_zdj_id_auta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auta_zdj
    ADD CONSTRAINT auta_zdj_id_auta_fkey FOREIGN KEY (id_auta) REFERENCES public.auta(id_auta) ON DELETE CASCADE;


--
-- TOC entry 3387 (class 2606 OID 16567)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3388 (class 2606 OID 16572)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3389 (class 2606 OID 16577)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3390 (class 2606 OID 16582)
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3391 (class 2606 OID 16587)
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3392 (class 2606 OID 16592)
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3393 (class 2606 OID 16597)
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3396 (class 2606 OID 16602)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3397 (class 2606 OID 16607)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3394 (class 2606 OID 16612)
-- Name: czarna_lista fk_admin_blacklist; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.czarna_lista
    ADD CONSTRAINT fk_admin_blacklist FOREIGN KEY (id_admin) REFERENCES public.admin(id_admin) ON DELETE SET NULL;


--
-- TOC entry 3399 (class 2606 OID 16617)
-- Name: wypozyczenie fk_auto; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.wypozyczenie
    ADD CONSTRAINT fk_auto FOREIGN KEY (id_auta) REFERENCES public.auta(id_auta) ON DELETE CASCADE;


--
-- TOC entry 3398 (class 2606 OID 16622)
-- Name: uzytkownicy fk_miasta; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.uzytkownicy
    ADD CONSTRAINT fk_miasta FOREIGN KEY (id_zamieszkania) REFERENCES public.miasta(id_zamieszkania) ON DELETE CASCADE;


--
-- TOC entry 3395 (class 2606 OID 16627)
-- Name: czarna_lista fk_user_blacklist; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.czarna_lista
    ADD CONSTRAINT fk_user_blacklist FOREIGN KEY (id_user) REFERENCES public.uzytkownicy(id_user) ON DELETE CASCADE;


--
-- TOC entry 3400 (class 2606 OID 16632)
-- Name: wypozyczenie fk_uzytkownik; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.wypozyczenie
    ADD CONSTRAINT fk_uzytkownik FOREIGN KEY (id_user) REFERENCES public.uzytkownicy(id_user) ON DELETE CASCADE;


-- Completed on 2025-04-17 12:50:05

--
-- PostgreSQL database dump complete
--

