
            set terminal png size 700,500 truecolor
            set output "./5.Analisis_mapeo/informe_mapeo-quals2.png"
            set grid xtics ytics y2tics back lc rgb "#cccccc"
            set multiplot
             set rmargin 0; set lmargin 0; set tmargin 0; set bmargin 0; set origin 0.1,0.1; set size 0.4,0.8
            set yrange [0:50]
            set ylabel "Quality"
            set xlabel "Cycle (fwd reads)"
            plot '-' using 1:2:3 with filledcurve lt 1 lc rgb "#cccccc" t '25-75th percentile' , '-' using 1:2 with lines lc rgb "#000000" t 'Median', '-' using 1:2 with lines lt 1 t 'Mean'
        1	41	41
2	41	41
3	41	41
4	41	41
5	41	41
6	41	41
7	41	41
8	41	41
9	41	41
10	41	41
11	41	41
12	41	41
13	41	41
14	41	41
15	41	41
16	41	41
17	41	41
18	41	41
19	41	41
20	41	41
21	41	41
22	41	41
23	41	41
24	41	41
25	41	41
26	41	41
27	41	41
28	41	41
29	41	41
30	41	41
31	41	41
32	41	41
33	41	41
34	41	41
35	41	41
36	41	41
37	41	41
38	41	41
39	41	41
40	41	41
41	41	41
42	41	41
43	41	41
44	41	41
45	41	41
46	41	41
47	41	41
48	41	41
49	41	41
50	41	41
51	41	41
52	41	41
53	41	41
54	41	41
55	41	41
56	41	41
57	41	41
58	41	41
59	41	41
60	41	41
61	41	41
62	41	41
63	41	41
64	41	41
65	41	41
66	41	41
67	41	41
68	41	41
69	41	41
70	41	41
71	41	41
72	41	41
73	41	41
74	41	41
75	41	41
76	41	41
77	41	41
78	41	41
79	41	41
80	41	41
81	41	41
82	41	41
83	41	41
84	41	41
85	41	41
86	41	41
87	41	41
88	41	41
89	41	41
90	41	41
91	41	41
92	41	41
93	41	41
94	41	41
95	41	41
96	41	41
97	41	41
98	41	41
99	41	41
100	41	41
101	41	41
102	41	41
103	41	41
104	41	41
105	41	41
106	41	41
107	41	41
108	41	41
109	41	41
110	41	41
111	41	41
112	41	41
113	41	41
114	41	41
115	41	41
116	41	41
117	41	41
118	41	41
119	41	41
120	41	41
121	41	41
122	41	41
123	41	41
124	41	41
125	41	41
126	41	41
127	41	41
128	41	41
129	41	41
130	41	41
131	41	41
132	41	41
133	41	41
134	41	41
135	41	41
136	41	41
137	41	41
138	41	41
139	41	41
140	41	41
141	41	41
142	37	41
end
1	41
2	41
3	41
4	41
5	41
6	41
7	41
8	41
9	41
10	41
11	41
12	41
13	41
14	41
15	41
16	41
17	41
18	41
19	41
20	41
21	41
22	41
23	41
24	41
25	41
26	41
27	41
28	41
29	41
30	41
31	41
32	41
33	41
34	41
35	41
36	41
37	41
38	41
39	41
40	41
41	41
42	41
43	41
44	41
45	41
46	41
47	41
48	41
49	41
50	41
51	41
52	41
53	41
54	41
55	41
56	41
57	41
58	41
59	41
60	41
61	41
62	41
63	41
64	41
65	41
66	41
67	41
68	41
69	41
70	41
71	41
72	41
73	41
74	41
75	41
76	41
77	41
78	41
79	41
80	41
81	41
82	41
83	41
84	41
85	41
86	41
87	41
88	41
89	41
90	41
91	41
92	41
93	41
94	41
95	41
96	41
97	41
98	41
99	41
100	41
101	41
102	41
103	41
104	41
105	41
106	41
107	41
108	41
109	41
110	41
111	41
112	41
113	41
114	41
115	41
116	41
117	41
118	41
119	41
120	41
121	41
122	41
123	41
124	41
125	41
126	41
127	41
128	41
129	41
130	41
131	41
132	41
133	41
134	41
135	41
136	41
137	41
138	41
139	41
140	41
141	41
142	41
end
1	41.39
2	41.38
3	41.38
4	41.35
5	41.30
6	41.29
7	41.29
8	41.23
9	41.25
10	41.26
11	41.23
12	41.26
13	41.23
14	41.23
15	41.21
16	41.21
17	41.22
18	41.23
19	41.19
20	41.18
21	41.16
22	41.16
23	41.15
24	41.16
25	41.16
26	41.16
27	41.16
28	41.15
29	41.13
30	41.12
31	41.15
32	41.12
33	41.11
34	41.11
35	41.10
36	41.13
37	41.11
38	41.08
39	41.08
40	41.07
41	41.06
42	41.07
43	41.06
44	41.04
45	41.02
46	41.02
47	41.02
48	41.01
49	40.96
50	40.95
51	40.95
52	40.95
53	40.94
54	40.97
55	40.96
56	40.95
57	40.90
58	40.91
59	40.92
60	40.94
61	40.93
62	40.92
63	40.91
64	40.89
65	40.88
66	40.86
67	40.25
68	40.57
69	40.73
70	40.80
71	40.82
72	40.84
73	40.83
74	40.85
75	40.86
76	40.84
77	40.81
78	40.81
79	40.80
80	40.77
81	40.77
82	40.75
83	40.76
84	40.75
85	40.73
86	40.70
87	40.68
88	40.70
89	40.70
90	40.69
91	40.68
92	40.67
93	40.66
94	40.62
95	40.60
96	40.60
97	40.57
98	40.55
99	40.56
100	40.55
101	40.54
102	40.51
103	40.55
104	40.53
105	40.52
106	40.46
107	40.49
108	40.50
109	40.47
110	40.45
111	40.40
112	40.43
113	40.39
114	40.42
115	40.39
116	40.37
117	40.35
118	40.35
119	40.30
120	40.31
121	40.27
122	40.19
123	40.23
124	40.25
125	40.23
126	40.16
127	40.16
128	40.13
129	40.13
130	40.10
131	40.12
132	40.12
133	40.12
134	40.12
135	40.15
136	40.21
137	40.24
138	40.34
139	40.54
140	40.58
141	40.58
142	39.30
end

                set origin 0.55,0.1
                set size 0.4,0.8
                unset ytics
                set y2tics mirror
                set yrange [0:50]
                unset ylabel
                set xlabel "Cycle (rev reads)"
                set label "analisis_mapeo.txt" at screen 0.5,0.95 center noenhanced
                plot '-' using 1:2:3 with filledcurve lt 1 lc rgb "#cccccc" t '25-75th percentile' , '-' using 1:2 with lines lc rgb "#000000" t 'Median', '-' using 1:2 with lines lt 2 t 'Mean'
            1	41	41
2	41	41
3	41	41
4	41	41
5	41	41
6	41	41
7	41	41
8	41	41
9	41	41
10	41	41
11	41	41
12	41	41
13	41	41
14	41	41
15	41	41
16	41	41
17	41	41
18	41	41
19	41	41
20	41	41
21	41	41
22	41	41
23	41	41
24	41	41
25	41	41
26	41	41
27	41	41
28	41	41
29	41	41
30	41	41
31	41	41
32	41	41
33	41	41
34	41	41
35	41	41
36	41	41
37	41	41
38	41	41
39	41	41
40	41	41
41	41	41
42	41	41
43	41	41
44	41	41
45	41	41
46	41	41
47	41	41
48	41	41
49	41	41
50	41	41
51	41	41
52	41	41
53	41	41
54	41	41
55	41	41
56	41	41
57	41	41
58	41	41
59	41	41
60	41	41
61	41	41
62	41	41
63	41	41
64	41	41
65	41	41
66	41	41
67	37	41
68	41	41
69	41	41
70	41	41
71	41	41
72	41	41
73	41	41
74	41	41
75	41	41
76	41	41
77	41	41
78	41	41
79	41	41
80	41	41
81	41	41
82	41	41
83	41	41
84	41	41
85	41	41
86	41	41
87	41	41
88	41	41
89	41	41
90	41	41
91	41	41
92	41	41
93	41	41
94	41	41
95	41	41
96	41	41
97	41	41
98	41	41
99	41	41
100	41	41
101	37	41
102	37	41
103	37	41
104	37	41
105	37	41
106	37	41
107	37	41
108	37	41
109	37	41
110	37	41
111	37	41
112	37	41
113	37	41
114	37	41
115	37	41
116	37	41
117	37	41
118	37	41
119	37	41
120	37	41
121	37	41
122	37	41
123	37	41
124	37	41
125	37	41
126	37	41
127	37	41
128	37	41
129	37	41
130	37	41
131	37	41
132	37	41
133	37	41
134	37	41
135	37	41
136	37	41
137	37	41
138	37	41
139	37	41
140	37	41
141	37	41
142	32	41
end
1	41
2	41
3	41
4	41
5	41
6	41
7	41
8	41
9	41
10	41
11	41
12	41
13	41
14	41
15	41
16	41
17	41
18	41
19	41
20	41
21	41
22	41
23	41
24	41
25	41
26	41
27	41
28	41
29	41
30	41
31	41
32	41
33	41
34	41
35	41
36	41
37	41
38	41
39	41
40	41
41	41
42	41
43	41
44	41
45	41
46	41
47	41
48	41
49	41
50	41
51	41
52	41
53	41
54	41
55	41
56	41
57	41
58	41
59	41
60	41
61	41
62	41
63	41
64	41
65	41
66	41
67	41
68	41
69	41
70	41
71	41
72	41
73	41
74	41
75	41
76	41
77	41
78	41
79	41
80	41
81	41
82	41
83	41
84	41
85	41
86	41
87	41
88	41
89	41
90	41
91	41
92	41
93	41
94	41
95	41
96	41
97	41
98	41
99	41
100	41
101	41
102	41
103	41
104	41
105	41
106	41
107	41
108	41
109	41
110	41
111	41
112	41
113	41
114	41
115	41
116	41
117	41
118	41
119	41
120	41
121	41
122	41
123	41
124	41
125	41
126	41
127	41
128	41
129	41
130	41
131	41
132	41
133	41
134	41
135	41
136	41
137	41
138	41
139	41
140	41
141	41
142	41
end
1	41.18
2	41.10
3	41.09
4	41.05
5	40.94
6	40.97
7	40.93
8	40.79
9	40.88
10	40.88
11	40.88
12	40.85
13	40.83
14	40.85
15	40.85
16	40.80
17	40.80
18	40.82
19	40.83
20	40.81
21	40.80
22	40.80
23	40.79
24	40.74
25	40.78
26	40.77
27	40.72
28	40.73
29	40.70
30	40.72
31	40.70
32	40.70
33	40.64
34	40.66
35	40.66
36	40.63
37	40.63
38	40.63
39	40.63
40	40.60
41	40.55
42	40.55
43	40.52
44	40.44
45	40.48
46	40.50
47	40.49
48	40.44
49	40.43
50	40.41
51	40.41
52	40.38
53	40.41
54	40.37
55	40.39
56	40.37
57	40.32
58	40.30
59	40.27
60	40.27
61	40.24
62	40.24
63	40.25
64	40.26
65	40.26
66	40.23
67	39.38
68	39.84
69	39.99
70	40.10
71	40.17
72	40.20
73	40.13
74	40.14
75	40.17
76	40.13
77	40.13
78	40.16
79	40.12
80	40.08
81	40.05
82	40.07
83	40.08
84	40.02
85	39.99
86	39.82
87	39.89
88	39.92
89	39.92
90	39.90
91	39.93
92	39.90
93	39.89
94	39.87
95	39.84
96	39.80
97	39.77
98	39.77
99	39.70
100	39.72
101	39.65
102	39.63
103	39.67
104	39.65
105	39.60
106	39.48
107	39.44
108	39.30
109	39.38
110	39.45
111	39.39
112	39.41
113	39.36
114	39.36
115	39.36
116	39.32
117	39.31
118	39.30
119	39.28
120	39.28
121	39.25
122	39.22
123	39.26
124	39.23
125	39.25
126	39.14
127	39.08
128	39.15
129	39.07
130	39.07
131	39.09
132	39.08
133	39.06
134	39.10
135	39.18
136	39.22
137	39.31
138	39.55
139	39.84
140	39.89
141	39.89
142	37.73
end