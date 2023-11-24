--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Debian 16.0-1.pgdg120+1)
-- Dumped by pg_dump version 16.0 (Debian 16.0-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: image_type; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.image_type AS ENUM (
    'link',
    'blob'
);


ALTER TYPE public.image_type OWNER TO "user";

--
-- Name: winner; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.winner AS ENUM (
    'white',
    'black'
);


ALTER TYPE public.winner OWNER TO "user";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.auth (
    id integer NOT NULL,
    "user" character varying,
    is_active boolean,
    salt character varying,
    hashed_password character varying
);


ALTER TABLE public.auth OWNER TO "user";

--
-- Name: auth_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.auth_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_id_seq OWNER TO "user";

--
-- Name: auth_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.auth_id_seq OWNED BY public.auth.id;


--
-- Name: game; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.game (
    game_id integer NOT NULL,
    white_player character varying,
    black_player character varying,
    fen character varying,
    moves character varying,
    is_finish boolean,
    winner public.winner,
    white_points integer,
    black_points integer
);


ALTER TABLE public.game OWNER TO "user";

--
-- Name: game_game_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.game_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.game_game_id_seq OWNER TO "user";

--
-- Name: game_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.game_game_id_seq OWNED BY public.game.game_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.users (
    "user" character varying NOT NULL,
    profile_image bytea,
    profile_image_url character varying,
    profile_image_type public.image_type,
    rating integer,
    wins integer,
    losses integer
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: auth id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.auth ALTER COLUMN id SET DEFAULT nextval('public.auth_id_seq'::regclass);


--
-- Name: game game_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.game ALTER COLUMN game_id SET DEFAULT nextval('public.game_game_id_seq'::regclass);


--
-- Data for Name: auth; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.auth (id, "user", is_active, salt, hashed_password) FROM stdin;
1	gio	t	88dafc30c3c6db2846324a71244f4e4c	$2b$12$nh8AT29VdTG/qUYgnsCxQ.83sYU1TBgEzD1kOGfKrKOJQhVGs0lAu
2	pische	t	d7de8b86cf0d06a15babf3ebe1387c49	$2b$12$x5Z0crxLiMRrjt8QHC/BROb6DPbxce0ffu9/duXX2xQx9OgV0S5jO
3	angi	t	e65c4f4b4dda569111757d96448cc5d4	$2b$12$8Y7tuxd2jC5AEqoHjpRVPOTR99hFWhbnOcWJtzmZPyDis7.qXfvP2
4	fil	t	3fce5012f9319a7c523807f85ffaa834	$2b$12$Rs6ajmtlWapPBlWf9XVPU.V7BoD58HE4STxUvTMSy0RppF3Laaw/W
5	diego	t	e3beb5626ee798ab8e8a396972df358d	$2b$12$2kWlqfjyjFWKavEfb0EZdOQWO1LBb0YD7A4Tm0VL00GgmkKWalF9O
6	alle	t	2055aa2e72e87ef62fc35174b9f75996	$2b$12$dakl0LKWbfA8.vpdWCL.AOHAHnDEABqYokICIc/FpmbetdvccNEXa
7	berny	t	913e7a50bf4062a084ed20493003653b	$2b$12$CLqkLO.mEGChY7.cM3upAOgmfGUMvb2u4gv5QGdXr4kqf1Ynxz0c.
8	carlsen	t	5a87cc647912b1d38337ae0eab7d20a2	$2b$12$KMZb4R5R8uB64JFCH6M6ruChmfNoPIGL8ssZVXyVSzIaHfjRYuPQ6
9	angelo-huang	t	bdac9d346a35a13e917f556d944393c3	$2b$12$FWTUoweFhoRNpNvSWWmK9uoluRGPiuHBa7SrVW/av5IBQ26d3OzwW
10	AlleNeri	t	d495587f15b2e9a23ffe5628e367039a	$2b$12$DsfQJRRiwQg4OHq5n2AkcuvgYtN/8b2sy1rf6y2QswH6a88kwb.uS
\.


--
-- Data for Name: game; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.game (game_id, white_player, black_player, fen, moves, is_finish, winner, white_points, black_points) FROM stdin;
1	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
2	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
3	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
4	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
5	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
6	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
7	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
27	gio	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
8	gio	carlsen	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
9	gio	angi	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
49	angelo-huang	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
10	gio	carlsen	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
11	gio	fil	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
28	gio	carlsen	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1560	1484
12	gio	angi	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
13	gio	diego	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
14	gio	fil	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
53	alle	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1491	1451
15	gio	alle	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
29	gio	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1573	1485
16	gio	alle	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
17	angi	pische	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
39	gio	carlsen	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1629	1471
30	gio	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1585	1485
19	berny	fil	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
18	gio	carlsen	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1500	1500
20	alle	diego	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
45	alle	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1495	1450
21	gio	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1516	1500
40	angelo-huang	\N	rnbqk1nr/pppp1ppp/8/4P3/4P3/8/PPP2PPP/RNBQbBNR w KQkq - 0 4	e2e4,e7e5,d2d4,f8b4,d4e5,b4e1	t	white	\N	\N
22	berny	angi	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
33	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
32	gio	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1597	1486
23	gio	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1531	1500
34	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
24	alle	fil	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
41	alle	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1479	1475
25	gio	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1546	1500
26	gio	alle	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
35	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1608	1500
31	\N	\N	r1bqkb1r/ppppp2p/4p1p1/n7/4n3/8/PPPP1PPP/RNBQ1BNR w kq - 0 7	e2e4,g7g6,e4e5,b8c6,e5e6,f7e6,e1e2,c6a5,e2e3,g8f6,e3e4,f6e4	t	white	\N	\N
36	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1619	1489
42	gio	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1638	1490
37	angi	pische	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1473	1500
50	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1673	1500
46	gio	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1656	1459
38	berny	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1500	1473
43	berny	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1515	1480
56	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
44	gio	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1648	1458
47	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1664	1509
52	berny	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1529	1436
54	berny	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1541	1483
51	angi	pische	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1466	1483
48	gio	angelo-huang	8/p6k/8/1p6/3p4/2B2pP1/PP6/1r6 w - - 0 28	d2d4,d7d5,d1d3,c8g4,c2c3,e7e5,h2h3,c7c6,h3g4,f8b4,c3b4,b8a6,c1d2,g7g5,d4e5,d8e7,g1f3,e7e5,f3e5,a6b4,d2b4,g8f6,e5f7,e8f7,b1c3,f6g4,e1c1,g4f2,d3e3,f7g6,e3f2,g5g4,f2c5,h8f8,c3b5,c6b5,d1d5,a8e8,c5c6,b7c6,b4c3,c6d5,h1h7,g6h7,g2g3,f8f1,c1c2,e8e2,c2d3,d5d4,d3e2,f1b1,e2f3,g4f3	t	white	1682	1500
55	alle	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1505	1424
57	\N	\N	4Q1nr/pp2bp1p/8/4N3/1N4p1/7P/PPP1PP1P/R1BQKB1R b KQk - 0 12	d2d4,b8c6,b1c3,c6b4,g1f3,d7d5,c3d5,c8h3,g2h3,d8d6,d5b4,g7g6,f3e5,c7c5,d4c5,a8d8,c5d6,g6g5,d6e7,g5g4,e7d8q,f8e7,d8e8	t	white	\N	\N
58	\N	\N	rnb1k1nr/pppp3p/4P1p1/6B1/3P4/8/PPP1QPPP/RN2bBNR w KQkq - 0 7	d2d4,f7f5,e2e4,e7e6,e4f5,d8g5,c1g5,g7g6,f5e6,f8b4,d1e2,b4e1	t	white	\N	\N
63	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
59	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
60	AlleNeri	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
62	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
64	gio	carlsen	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-9000	1462
61	\N	\N	8/6B1/1NN5/2P5/4R3/P7/1R3PKP/8 b - - 0 43	e2e4,e7e6,g1f3,f8a3,d2d3,a3d6,c1e3,a7a5,b1c3,b7b5,d3d4,d8g5,e3g5,g8h6,g5h6,b5b4,c3e2,b4b3,a2b3,d6a3,b2a3,c8a6,e2c3,f7f5,f1a6,h8g8,h6g5,f5e4,c3e4,c7c5,e1g1,c5d4,f3d4,b8a6,e4c3,d7d6,d4e6,h7h6,e6g7,e1c1,g5h6,a6c7,g7e6,g8g2,g1g2,c7a6,e6d8,a5a4,d8b7,a6b8,b7d6,c8d8,d6f7,d8c7,c3d5,c7d7,d5b6,d7e6,f1e1,e6f5,c2c4,a4b3,c4c5,b3b2,a1b1,f5g6,b1b2,g6f5,d1d6,f5g4,e1e7,b8c6,f7e5,g4f5,e5c6,f5g4,e7e4,g4h5,d6f4,h5g6,f4g5,g6h7,g5g7,h7g7,h6g7	t	white	\N	\N
85	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
84	\N	\N	rnbqBb1r/ppp1pppp/3p4/8/3Pn3/8/PPP2PPP/RNBQK1NR b KQkq - 0 4	d2d4,d7d6,e2e4,g8f6,f1b5,f6e4,b5e8	t	white	\N	\N
65	gio	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8968	1470
86	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
66	gio	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8936	3578
87	\N	\N	6k1/1p3np1/n5p1/1b3P2/8/2PP3B/PP2P3/R3b1R1 w Q - 0 24	d2d3,d7d6,c1h6,d6d5,h6g5,c7c6,c2c3,c8f5,d1b3,f5e6,b3d5,e6d7,g5e7,d8a5,d5f7,e8f7,b1a3,g8h6,g1f3,f8e7,f3e5,a5e5,a3b5,e7d8,b5a7,f7g8,a7c6,a8a6,c6e5,a6g6,e5g6,h7g6,f2f4,h6f7,h2h4,d7c6,g2g3,b8a6,f1h3,h8h4,g3h4,c6b5,h1g1,d8h4,f4f5,h4e1	t	white	\N	\N
67	gio	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8904	1437
88	\N	\N	r1Qqk1nr/p3pp2/3pn1p1/2p4p/7P/R6R/1PPPP1P1/1NBQbBN1 w kq - 0 12	a2a3,b8c6,h2h3,h7h5,a3a4,c6d4,h3h4,d7d6,a1a3,d4e6,a4a5,g7g6,h1h3,c7c5,a5a6,f8g7,a6b7,g7d4,b7b8q,d4f2,b8c8,f2e1	t	white	\N	\N
68	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8872	1517
89	\N	\N	R7/2R5/2B5/p5p1/7p/7N/KP3PPP/8 b - - 0 39	d2d4,e7e5,d4e5,f8d6,e5d6,h7h5,d6c7,a7a6,c7d8q,e8d8,c2c4,g8e7,c4c5,d7d5,c5d6,g7g6,d6e7,d8c7,d1d8,h8d8,e7d8q,c7d8,b1c3,c8h3,g1h3,d8c8,c1f4,h5h4,f4b8,f7f5,e1c1,c8b8,e2e4,a6a5,c1c2,a8a6,d1d3,f5e4,c3e4,b7b6,f1e2,b8b7,c2b1,b7a8,h1d1,a8b8,e4d6,a6a7,d6c8,b6b5,c8a7,b8a8,d3d8,a8a7,d1d7,a7a6,d8a8,a6b6,d7d6,b6b7,a8a6,b7b8,a6c6,b5b4,e2b5,b4b3,d6d7,b3a2,b1a2,b8a8,c6a6,a8b8,b5c6,g6g5,a6a8,b8c7,d7c7	t	white	\N	\N
69	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8840	1485
91	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
90	\N	\N	6B1/2p5/7Q/6B1/8/p6p/PPPp1P1P/RN3K2 b - - 0 29	e2e4,d7d6,d1f3,b8c6,f3f7,e8f7,f1b5,f7e8,g1f3,e8f7,f3d4,f7g6,d4c6,a7a5,c6d8,g6f6,d8f7,a8a6,f7h8,c8h3,b5a6,h7h5,a6b7,h3g2,h1g1,g8h6,g1g2,d6d5,e4d5,g7g5,g2g5,a5a4,d2d4,e7e5,e1f1,f8g7,g5g7,f6g7,c1h6,g7h8,h6g5,h5h4,b7c6,h4h3,d5d6,e5d4,d6d7,a4a3,d7d8q,h8g7,d8f6,g7g8,f6h6,d4d3,c6d5,d3d2,d5g8	t	white	\N	\N
70	angi	pische	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1438	1466
92	gio	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
71	berny	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1554	3546
103	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8680	1499
72	alle	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1453	1405
93	gio	\N	6B1/8/3R4/8/N3P3/1N2K1P1/PP3P1P/5R2 b - - 0 43	e2e4,g7g5,f1c4,a7a5,d2d3,c7c6,c1d2,f8h6,d1h5,a8a6,c4a6,d8b6,a6c4,b6b4,c4f7,e8d8,d2b4,h6f8,b4e7,g8e7,f7g8,d8c7,g8h7,h8g8,h7g8,c7d8,h5g5,a5a4,b1c3,b8a6,c3d5,d7d6,g5e7,f8e7,d5e7,d8c7,e7c8,c7d8,c8b6,a6b4,b6a4,b4d3,c2d3,c6c5,a1c1,c5c4,c1c4,d6d5,g1f3,d5e4,d3e4,b7b5,e1e2,d8e7,h1d1,e7f8,c4c8,f8g7,d1d7,g7g6,c8c6,g6h5,d7d5,h5g4,g2g3,b5b4,c6g6,g4h3,d5h5,h3g2,e2d2,g2f1,d2e3,b4b3,f3d2,f1g2,g6d6,g2g1,d2b3,g1f1,h5d5,f1e1,d5d1,e1f1,d1f1	t	white	\N	\N
94	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
73	berny	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1586	1455
95	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
96	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
74	alle	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1467	3514
75	\N	\N	2q1k2r/2pn1p2/r3p1pp/2b1P3/4nP2/8/PPPP2PP/RNBQ2NR w k - 0 11	e2e4,a7a6,f1a6,g7g6,a6b7,h7h6,b7c8,e7e6,c8d7,b8d7,e4e5,d8c8,f2f4,a8a6,e1e2,g8f6,e2e3,f8c5,e3e4,f6e4	t	white	\N	\N
77	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
78	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
79	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
76	\N	\N	7Q/pp1k4/5p1p/3B1bp1/P1P1PPPP/B4N2/8/RN2n2R w KQ - 0 22	e2e4,c7c5,f2f4,c5c4,g2g4,h7h6,f1c4,d7d5,h2h4,c8f5,c4d5,b8c6,d2d4,a8b8,c2c4,f5h7,b2b4,c6b4,a2a4,e7e5,d1b3,e5d4,b3b4,d8f6,b4a5,g7g5,g1f3,f8a3,c1a3,f6b6,a5b6,f7f6,b6b4,h7f5,b4f8,e8d7,f8b8,d4d3,b8g8,d3d2,g8h8,d2e1n	t	white	\N	\N
80	\N	\N	8/8/8/6p1/1N1Q4/1BB1P3/1P3P1P/R3K1r1 b - - 0 42	d2d4,d7d5,d1d3,c8e6,d3g3,c7c5,d4c5,d5d4,c2c3,d4c3,b1c3,b8a6,c1d2,g8h6,d2h6,h8g8,h6d2,e6b3,a2b3,g7g6,e2e3,h7h5,f1a6,g6g5,a6d3,e7e5,c5c6,f7f6,c6b7,f8h6,b7a8q,g8g7,a8d8,e8d8,d3b5,a7a6,b5a6,d8d7,c3d5,e5e4,g3c7,d7e8,d2c3,f6f5,c7f4,h5h4,f4f5,g7b7,a6b7,e8d8,a1a8,h6g7,f5h7,d8d7,h7g7,d7d6,g7f6,d6c5,a8a5,c5c4,f6f5,c4b3,f5e4,h4h3,e4b4,b3c2,a5a1,h3g2,b4d4,g2h1r,d4d2,c2b3,d2d1,b3c4,d1a4,c4d3,a4d4,d3c2,d5b4,c2b3,b7d5,h1g1,d5b3	t	white	\N	\N
97	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
81	gio	\N	r1bqBb1r/1pp2ppp/p4n2/3pN3/8/4P3/PPP2PPP/RNBQK2R b KQkq - 0 7	d2d4,d7d5,e2e3,e7e5,g1f3,b8c6,d4e5,c6e5,f3e5,g8f6,f1b5,a7a6,b5e8	t	white	\N	\N
98	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
82	gio	\N	rnbqBbnr/ppp1pppp/8/8/4p3/8/PPPP1PPP/RNBQK1NR b KQkq - 0 3	e2e4,d7d5,f1b5,d5e4,b5e8	t	white	\N	\N
83	\N	gio	4kb1r/3n1ppp/2p2n2/8/2BPP3/5P2/Pp1B2PP/3R3R w k - 0 20	d2d4,d7d5,b1c3,c7c6,c1d2,e7e6,c3d5,e6d5,c2c4,c8d7,c4d5,d8e7,d1a4,e7d6,e1c1,g8f6,g1f3,b7b5,a4a5,d6d5,a5b5,d5b5,f3e5,b5b2,c1b2,a7a5,b2a1,a5a4,e5d7,b8d7,e2e4,a4a3,f1c4,a8b8,f2f3,b8b2,a1b2,a3b2	t	white	\N	\N
104	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8648	1467
99	gio	carlsen	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8808	1430
101	gio	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8744	3482
100	gio	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8776	1445
102	gio	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8712	1391
105	angi	pische	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1413	1449
106	berny	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1596	3450
107	alle	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1435	1359
108	berny	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1628	1431
109	alle	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1448	3418
110	gio	carlsen	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8616	1398
111	gio	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8584	1423
112	gio	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8552	3386
113	gio	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8520	1346
114	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8488	1480
115	gio	alle	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	-8456	1448
116	angi	pische	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1391	1431
117	berny	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1636	3354
118	alle	diego	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1416	1314
119	berny	angi	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1668	1409
120	alle	fil	rnbqQbnr/1pppp1pp/p7/5p2/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3	e2e4,f7f5,d1h5,a7a6,h5e8	t	white	1427	3322
121	\N	\N	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1		f	\N	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.users ("user", profile_image, profile_image_url, profile_image_type, rating, wins, losses) FROM stdin;
angelo-huang	\N	https://api.dicebear.com/7.x/lorelei/png?seed=angelo-huang	link	1492	0	1
AlleNeri	\N	https://api.dicebear.com/7.x/lorelei/png?seed=AlleNeri	link	1500	0	0
gio	\N	https://api.dicebear.com/7.x/lorelei/png?seed=gio	link	-8424	18	42184421
pische	\N	https://api.dicebear.com/7.x/lorelei/png?seed=pische	link	1413	0	5
diego	\N	https://api.dicebear.com/7.x/lorelei/png?seed=diego	link	1303	0	11
angi	\N	https://api.dicebear.com/7.x/lorelei/png?seed=angi	link	1403	5	11
berny	\N	https://api.dicebear.com/7.x/lorelei/png?seed=berny	link	1674	10	0
alle	\N	https://api.dicebear.com/7.x/lorelei/png?seed=alle	link	1459	10	10
fil	\N	https://api.dicebear.com/7.x/lorelei/png?seed=fil	link	3290	7920	9
carlsen	\N	https://api.dicebear.com/7.x/lorelei/png?seed=carlsen	link	1366	0	6
\.


--
-- Name: auth_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.auth_id_seq', 10, true);


--
-- Name: game_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.game_game_id_seq', 121, true);


--
-- Name: auth auth_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.auth
    ADD CONSTRAINT auth_pkey PRIMARY KEY (id);


--
-- Name: game game_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_pkey PRIMARY KEY (game_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("user");


--
-- Name: ix_auth_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_auth_id ON public.auth USING btree (id);


--
-- Name: ix_auth_user; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_auth_user ON public.auth USING btree ("user");


--
-- Name: ix_users_user; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_users_user ON public.users USING btree ("user");


--
-- Name: auth auth_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.auth
    ADD CONSTRAINT auth_user_fkey FOREIGN KEY ("user") REFERENCES public.users("user");


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO "user";


--
-- PostgreSQL database dump complete
--

