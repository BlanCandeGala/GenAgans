
            set terminal png size 600,400 truecolor
            set output "./5.Analisis_mapeo/informe_mapeo-gc-content.png"
            set grid xtics ytics y2tics back lc rgb "#cccccc"
            set title "analisis_mapeo.txt" noenhanced
            set ylabel "Normalized Frequency"
            set xlabel "GC Content [%]"
            set yrange [0:1.1]
            set label sprintf("%.1f",48.99) at 48.99,1 front offset 1,0
            plot '-' smooth csplines with lines lc 1 title 'First fragments' , '-' smooth csplines with lines lc 2 title 'Last fragments'
        3	0.000000
6	0.000002
9	0.000000
11	0.000007
12	0.000010
13	0.000005
14	0.000002
14	0.000005
15	0.000007
16	0.000015
17	0.000027
17	0.000051
18	0.000071
18	0.000110
19	0.000139
19	0.000259
20	0.000332
20	0.000440
21	0.000681
21	0.000923
22	0.001521
22	0.001795
23	0.002598
23	0.004041
24	0.004794
24	0.006464
25	0.009145
25	0.012847
26	0.015021
26	0.021414
27	0.028293
27	0.031431
28	0.041943
28	0.055784
29	0.070812
29	0.079389
30	0.099398
30	0.123986
31	0.136597
31	0.168679
32	0.204457
32	0.245955
33	0.264431
33	0.315498
34	0.368804
34	0.392847
35	0.450771
35	0.515986
36	0.577734
36	0.600098
37	0.657645
37	0.707989
38	0.726812
38	0.775585
39	0.814478
39	0.854283
40	0.867105
40	0.892018
41	0.915442
41	0.921964
42	0.932240
42	0.942601
43	0.952342
43	0.954211
44	0.956914
44	0.966276
45	0.969834
45	0.975834
46	0.980420
46	0.983534
47	0.986071
47	0.993031
48	0.997182
48	1.000000
49	0.996440
50	0.993438
50	0.974205
51	0.962330
51	0.942472
52	0.904663
52	0.885745
53	0.841081
53	0.793546
54	0.742733
54	0.724311
55	0.679061
55	0.636522
56	0.625455
56	0.587321
57	0.548054
57	0.511767
58	0.498495
58	0.470871
59	0.439719
59	0.427309
60	0.409094
60	0.393446
61	0.380030
61	0.376179
62	0.378689
62	0.377927
63	0.376542
63	0.383734
64	0.383478
64	0.381800
65	0.379392
65	0.373915
66	0.357414
66	0.352425
67	0.334555
67	0.307581
68	0.276942
68	0.271091
69	0.242791
69	0.214923
70	0.206750
70	0.177072
71	0.148198
71	0.122309
72	0.112658
72	0.091811
73	0.074177
73	0.068292
74	0.053274
74	0.041272
75	0.033834
75	0.030893
76	0.023050
76	0.017948
77	0.016022
77	0.012459
78	0.010159
78	0.008300
79	0.007135
79	0.005001
80	0.003697
80	0.003126
81	0.002117
81	0.001458
82	0.001179
82	0.001052
83	0.000813
83	0.000606
84	0.000435
84	0.000271
85	0.000147
85	0.000076
86	0.000061
86	0.000027
87	0.000007
87	0.000005
88	0.000002
89	0.000005
91	0.000000
93	0.000002
end
3	0.000000
6	0.000002
9	0.000000
12	0.000002
12	0.000010
13	0.000007
13	0.000005
14	0.000000
15	0.000005
15	0.000007
16	0.000015
16	0.000027
17	0.000020
17	0.000044
18	0.000071
18	0.000132
19	0.000181
19	0.000277
20	0.000392
20	0.000519
21	0.000778
21	0.001047
22	0.001574
22	0.001943
23	0.002971
23	0.004258
24	0.005105
24	0.006805
25	0.010090
25	0.014174
26	0.016594
26	0.022856
27	0.029924
27	0.034015
28	0.044827
28	0.059235
29	0.074138
29	0.083944
30	0.104909
30	0.129713
31	0.144773
31	0.175418
32	0.213461
32	0.254306
33	0.275327
33	0.326370
34	0.374698
34	0.403043
35	0.463414
35	0.526139
36	0.584547
36	0.613318
37	0.669527
37	0.722140
38	0.746714
38	0.787043
39	0.824993
39	0.863325
40	0.877347
40	0.904909
41	0.923064
41	0.931363
42	0.942414
42	0.950377
43	0.958465
43	0.960914
44	0.968026
44	0.974958
45	0.978032
45	0.981353
46	0.991971
46	0.988799
47	0.992497
47	0.997130
48	0.995952
48	1.000000
49	0.999672
50	0.992238
50	0.979089
51	0.966694
51	0.943853
52	0.906825
52	0.886534
53	0.844002
53	0.799653
54	0.755443
54	0.731163
55	0.686581
55	0.648542
56	0.634072
56	0.596428
57	0.558233
57	0.526244
58	0.512056
58	0.481489
59	0.452047
59	0.436828
60	0.418201
60	0.402635
61	0.390406
61	0.385279
62	0.386523
62	0.388434
63	0.386919
63	0.387411
64	0.388762
64	0.387653
65	0.384134
65	0.376788
66	0.363140
66	0.355821
67	0.337893
67	0.313613
68	0.286288
68	0.275861
69	0.248952
69	0.223531
70	0.211325
70	0.180564
71	0.153910
71	0.129084
72	0.115710
72	0.096679
73	0.079084
73	0.069905
74	0.056893
74	0.044185
75	0.035413
75	0.032013
76	0.024993
76	0.019384
77	0.016871
77	0.013285
78	0.010983
78	0.008888
79	0.007520
79	0.005269
80	0.004126
80	0.003365
81	0.002288
81	0.001644
82	0.001314
82	0.001187
83	0.000940
83	0.000685
84	0.000519
84	0.000289
85	0.000196
85	0.000137
86	0.000095
86	0.000051
87	0.000022
87	0.000017
88	0.000012
88	0.000007
89	0.000005
90	0.000012
90	0.000010
91	0.000002
94	0.000000
97	0.000002
end
