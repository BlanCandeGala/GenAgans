
            set terminal png size 600,400 truecolor
            set output "./5.Analisis_mapeo/informe_mapeo-coverage.png"
            set grid xtics ytics y2tics back lc rgb "#cccccc"
            set ylabel "Number of mapped bases"
            set xlabel "Coverage"
            set log y
            set style fill solid border -1
            set title "analisis_mapeo.txt" noenhanced
            set xrange [:141]
            plot '-' with lines notitle
        1	82009681
2	253149525
3	30174821
4	103415970
5	14982135
6	45087752
7	8239655
8	21476083
9	4966434
10	11414502
11	3266699
12	6805184
13	2384687
14	4493116
15	1843931
16	3203288
17	1490918
18	2443987
19	1267917
20	1933776
21	1080264
22	1601864
23	950203
24	1348603
25	845065
26	1152781
27	762771
28	1007148
29	682637
30	887434
31	623098
32	779668
33	562393
34	699788
35	517168
36	627168
37	475089
38	563145
39	433276
40	514051
41	397917
42	466350
43	372326
44	427069
45	344837
46	387412
47	316158
48	355071
49	293247
50	324248
51	270542
52	300652
53	254422
54	278615
55	232717
56	256480
57	218988
58	234918
59	204567
60	216392
61	189492
62	198922
63	177938
64	185142
65	166442
66	175044
67	155103
68	163273
69	147641
70	153187
71	135737
72	142928
73	126877
74	132366
75	120445
76	123799
77	113105
78	114638
79	105940
80	110661
81	101257
82	103902
83	94792
84	95437
85	89206
86	90693
87	83713
88	84221
89	79775
90	80193
91	74821
92	74582
93	70816
94	71764
95	68337
96	67907
97	64377
98	64811
99	60628
100	61736
101	56662
102	57550
103	54678
104	54328
105	52000
106	52432
107	48821
108	49287
109	46390
110	46892
111	44281
112	43715
113	41253
114	41998
115	40129
116	39821
117	38344
118	38629
119	36252
120	36288
121	34294
122	34031
123	32757
124	32480
125	30946
126	30260
127	30125
128	29106
129	28257
130	28027
131	27368
132	27283
133	25934
134	25900
135	25032
136	24202
137	23587
138	23265
139	22264
140	21806
141	21104
142	21222
143	21085
144	20841
145	20481
146	19368
147	19164
148	18850
149	17717
150	17816
151	17481
152	17329
153	16728
154	16201
155	15722
156	15735
157	15378
158	14606
159	14229
160	14152
161	13786
162	13869
163	13176
164	13132
165	12568
166	12640
167	12217
168	12943
169	11972
170	11821
171	11566
172	11398
173	10902
174	10891
175	10639
176	10593
177	10669
178	10091
179	10073
180	9618
181	9474
182	9250
183	9306
184	8939
185	8818
186	8251
187	8543
188	8483
189	8261
190	7893
191	7852
192	7687
193	7351
194	7090
195	7160
196	7106
197	6783
198	6644
199	6542
200	6532
201	6601
202	6219
203	6334
204	6452
205	6406
206	6211
207	5846
208	5862
209	5843
210	5568
211	5382
212	5568
213	5273
214	5217
215	5163
216	5202
217	4801
218	4809
219	4869
220	4678
221	4391
222	4490
223	4471
224	4540
225	4295
226	4222
227	4274
228	4112
229	4202
230	4101
231	3827
232	3684
233	3633
234	3641
235	3539
236	3446
237	3554
238	3447
239	3404
240	3479
241	3380
242	3452
243	3307
244	3288
245	3041
246	3186
247	3171
248	3004
249	2902
250	2813
251	2820
252	2858
253	2742
254	2935
255	2831
256	2640
257	2735
258	2646
259	2619
260	2372
261	2578
262	2625
263	2439
264	2430
265	2421
266	2319
267	2334
268	2304
269	2089
270	2236
271	2232
272	2240
273	2114
274	2017
275	2056
276	1967
277	1919
278	1945
279	2078
280	1930
281	1878
282	1845
283	1776
284	1795
285	1820
286	1772
287	1770
288	1761
289	1754
290	1682
291	1715
292	1607
293	1600
294	1780
295	1618
296	1581
297	1571
298	1570
299	1524
300	1412
301	1528
302	1455
303	1423
304	1513
305	1460
306	1334
307	1320
308	1434
309	1359
310	1329
311	1243
312	1327
313	1249
314	1351
315	1334
316	1293
317	1300
318	1291
319	1240
320	1153
321	1176
322	1213
323	1122
324	1141
325	1070
326	1098
327	1101
328	1083
329	1128
330	1152
331	1070
332	1042
333	1100
334	975
335	1039
336	967
337	1000
338	1063
339	1095
340	995
341	949
342	996
343	933
344	927
345	889
346	875
347	840
348	898
349	921
350	885
351	846
352	901
353	865
354	754
355	837
356	815
357	834
358	832
359	752
360	812
361	800
362	813
363	787
364	791
365	774
366	751
367	764
368	729
369	718
370	689
371	721
372	750
373	682
374	708
375	635
376	631
377	643
378	649
379	662
380	602
381	691
382	607
383	637
384	679
385	621
386	567
387	630
388	551
389	530
390	585
391	542
392	576
393	618
394	524
395	557
396	499
397	520
398	544
399	513
400	525
401	560
402	540
403	526
404	515
405	550
406	516
407	534
408	499
409	518
410	474
411	495
412	478
413	487
414	500
415	468
416	486
417	462
418	444
419	400
420	417
421	443
422	421
423	435
424	445
425	418
426	431
427	444
428	422
429	414
430	442
431	411
432	428
433	428
434	404
435	465
436	444
437	389
438	442
439	413
440	450
441	410
442	408
443	383
444	359
445	404
446	386
447	362
448	362
449	368
450	357
451	325
452	378
453	358
454	363
455	339
456	321
457	357
458	338
459	382
460	371
461	356
462	295
463	356
464	328
465	376
466	332
467	375
468	342
469	301
470	307
471	361
472	308
473	324
474	291
475	375
476	366
477	324
478	324
479	327
480	318
481	283
482	347
483	331
484	327
485	297
486	282
487	311
488	288
489	324
490	332
491	316
492	291
493	274
494	315
495	298
496	267
497	288
498	284
499	325
500	277
501	280
502	286
503	283
504	272
505	274
506	270
507	255
508	269
509	252
510	236
511	264
512	260
513	235
514	207
515	248
516	242
517	225
518	264
519	234
520	215
521	228
522	245
523	215
524	242
525	265
526	261
527	210
528	266
529	222
530	253
531	216
532	260
533	245
534	219
535	227
536	225
537	206
538	205
539	227
540	239
541	232
542	228
543	207
544	190
545	214
546	214
547	231
548	230
549	202
550	192
551	172
552	205
553	178
554	170
555	212
556	206
557	210
558	214
559	182
560	173
561	201
562	167
563	160
564	177
565	182
566	223
567	192
568	197
569	198
570	173
571	184
572	188
573	170
574	153
575	180
576	184
577	173
578	171
579	164
580	159
581	163
582	157
583	183
584	184
585	184
586	186
587	188
588	171
589	174
590	196
591	154
592	130
593	155
594	164
595	144
596	187
597	151
598	148
599	148
600	157
601	163
602	179
603	163
604	157
605	168
606	143
607	137
608	166
609	145
610	161
611	168
612	166
613	192
614	135
615	153
616	129
617	145
618	148
619	163
620	156
621	153
622	137
623	151
624	148
625	139
626	142
627	123
628	124
629	128
630	136
631	156
632	116
633	128
634	141
635	124
636	118
637	103
638	153
639	161
640	139
641	134
642	153
643	125
644	135
645	137
646	144
647	134
648	137
649	128
650	112
651	131
652	118
653	132
654	117
655	138
656	133
657	112
658	103
659	120
660	118
661	113
662	116
663	126
664	124
665	105
666	102
667	113
668	131
669	111
670	103
671	106
672	91
673	113
674	114
675	122
676	126
677	130
678	132
679	85
680	116
681	104
682	94
683	98
684	107
685	115
686	101
687	119
688	115
689	122
690	127
691	101
692	104
693	95
694	86
695	93
696	121
697	87
698	75
699	97
700	105
701	105
702	95
703	109
704	112
705	113
706	89
707	97
708	119
709	110
710	117
711	100
712	88
713	106
714	100
715	104
716	100
717	98
718	86
719	98
720	74
721	115
722	90
723	83
724	84
725	112
726	114
727	106
728	107
729	94
730	101
731	99
732	111
733	92
734	85
735	87
736	92
737	101
738	89
739	91
740	97
741	96
742	85
743	72
744	91
745	89
746	103
747	106
748	99
749	82
750	83
751	83
752	96
753	100
754	91
755	89
756	94
757	94
758	105
759	105
760	88
761	84
762	69
763	83
764	96
765	84
766	89
767	79
768	88
769	83
770	67
771	68
772	80
773	78
774	62
775	87
776	76
777	78
778	78
779	79
780	84
781	71
782	69
783	64
784	82
785	81
786	83
787	76
788	60
789	72
790	74
791	85
792	82
793	64
794	79
795	73
796	69
797	49
798	79
799	90
800	62
801	52
802	83
803	59
804	68
805	68
806	70
807	69
808	59
809	78
810	84
811	81
812	74
813	82
814	67
815	85
816	76
817	60
818	80
819	67
820	66
821	80
822	71
823	82
824	75
825	79
826	79
827	66
828	75
829	63
830	79
831	66
832	69
833	73
834	69
835	73
836	85
837	72
838	63
839	80
840	67
841	69
842	69
843	73
844	79
845	80
846	80
847	60
848	55
849	62
850	59
851	66
852	71
853	72
854	58
855	63
856	67
857	72
858	63
859	72
860	84
861	84
862	66
863	71
864	70
865	70
866	52
867	81
868	77
869	59
870	81
871	73
872	63
873	77
874	75
875	77
876	59
877	71
878	60
879	65
880	64
881	70
882	59
883	72
884	72
885	70
886	74
887	76
888	71
889	67
890	67
891	66
892	67
893	74
894	62
895	63
896	61
897	54
898	65
899	52
900	46
901	47
902	57
903	52
904	57
905	68
906	64
907	49
908	57
909	57
910	67
911	51
912	57
913	68
914	55
915	63
916	41
917	56
918	58
919	42
920	54
921	60
922	61
923	40
924	61
925	58
926	51
927	61
928	55
929	61
930	69
931	60
932	57
933	59
934	51
935	43
936	58
937	49
938	40
939	73
940	43
941	68
942	52
943	53
944	49
945	59
946	61
947	54
948	48
949	43
950	47
951	52
952	57
953	33
954	49
955	54
956	60
957	52
958	42
959	49
960	48
961	50
962	47
963	52
964	41
965	43
966	46
967	43
968	44
969	50
970	56
971	60
972	50
973	43
974	51
975	51
976	41
977	44
978	62
979	50
980	42
981	66
982	59
983	52
984	29
985	44
986	53
987	34
988	45
989	42
990	37
991	41
992	29
993	37
994	49
995	50
996	46
997	42
998	44
999	41
1000	55
1000	27680
end
