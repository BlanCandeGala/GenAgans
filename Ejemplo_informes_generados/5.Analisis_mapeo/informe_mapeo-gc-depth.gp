
            set terminal png size 600,500 truecolor
            set output "./5.Analisis_mapeo/informe_mapeo-gc-depth.png"
            set grid xtics ytics y2tics back lc rgb "#cccccc"
            set ylabel "Mapped depth"
            set xlabel "Percentile of mapped sequence ordered by GC content"
            set x2label "GC Content [%]"
            set title "analisis_mapeo.txt" noenhanced
            set x2tics ("30" 65.873,"40" 92.749,"50" 98.462)
            set xtics nomirror
            set xrange [0.1:99.9]

            plot '-' using 1:2:3 with filledcurve lt 1 lc rgb "#dedede" t '10-90th percentile' , \
                 '-' using 1:2:3 with filledcurve lt 1 lc rgb "#bbdeff" t '25-75th percentile' , \
                 '-' using 1:2 with lines lc rgb "#0084ff" t 'Median'
        0.161	0.007	0.082
0.164	0.165	0.213
0.167	0.103	0.144
0.175	0.084	0.244
0.186	0.056	0.192
0.202	0.050	0.220
0.221	0.055	0.231
0.234	0.041	0.384
0.250	0.041	0.265
0.269	0.054	0.650
0.300	0.031	0.906
0.354	0.070	0.786
0.418	0.075	1.022
0.520	0.195	1.111
0.697	0.218	1.155
0.986	0.414	1.129
1.498	0.467	1.194
2.280	0.521	1.221
3.495	0.555	1.242
5.212	0.569	1.323
7.671	0.583	1.338
10.919	0.611	1.372
15.096	0.624	1.434
20.252	0.645	1.482
26.164	0.645	1.537
32.658	0.672	1.599
39.589	0.686	1.667
46.584	0.707	1.777
53.406	0.734	1.921
59.904	0.755	2.099
65.873	0.796	2.381
71.047	0.830	2.669
75.638	0.885	3.081
79.429	0.974	3.478
82.574	1.036	4.008
85.195	1.142	4.652
87.353	1.262	5.070
89.042	1.420	6.022
90.460	1.530	6.577
91.677	1.619	7.052
92.749	1.750	7.842
93.684	1.880	8.932
94.492	1.949	9.791
95.212	2.072	10.862
95.861	2.174	10.272
96.446	2.342	11.677
96.959	2.397	12.165
97.406	2.404	11.894
97.806	2.600	12.281
98.141	2.715	13.798
98.462	2.792	13.557
98.738	3.138	14.731
98.976	3.399	13.858
99.225	3.492	14.147
99.412	3.736	17.292
99.564	3.915	17.367
99.686	4.159	14.998
99.780	4.858	16.546
99.858	5.763	18.923
99.913	4.804	21.697
99.942	6.283	23.635
99.969	5.942	25.291
99.988	5.670	28.359
99.996	3.591	37.858
99.999	9.749	15.026
100.000	12.803	14.477
end
0.161	0.014	0.055
0.164	0.166	0.204
0.167	0.105	0.137
0.175	0.089	0.144
0.186	0.075	0.158
0.202	0.067	0.170
0.221	0.089	0.158
0.234	0.081	0.233
0.250	0.060	0.160
0.269	0.089	0.288
0.300	0.075	0.578
0.354	0.117	0.631
0.418	0.144	0.772
0.520	0.473	0.878
0.697	0.551	0.925
0.986	0.597	0.933
1.498	0.617	1.015
2.280	0.672	1.036
3.495	0.686	1.036
5.212	0.714	1.084
7.671	0.727	1.125
10.919	0.748	1.146
15.096	0.768	1.187
20.252	0.796	1.228
26.164	0.810	1.269
32.658	0.830	1.317
39.589	0.858	1.365
46.584	0.885	1.441
53.406	0.926	1.523
59.904	0.967	1.633
65.873	1.029	1.791
71.047	1.084	1.969
75.638	1.194	2.271
79.429	1.324	2.559
82.574	1.407	2.991
85.195	1.573	3.403
87.353	1.760	3.787
89.042	1.990	4.221
90.460	2.147	4.617
91.677	2.298	5.009
92.749	2.566	5.585
93.684	2.648	6.003
94.492	2.871	6.415
95.212	3.005	6.978
95.861	3.022	7.094
96.446	3.389	7.715
96.959	3.455	8.086
97.406	3.566	8.214
97.806	3.835	8.775
98.141	3.835	9.631
98.462	4.075	9.293
98.738	4.693	9.166
98.976	4.559	10.099
99.225	5.108	10.521
99.412	5.492	12.075
99.564	5.607	11.647
99.686	5.379	11.170
99.780	6.305	11.787
99.858	6.796	12.978
99.913	6.775	16.696
99.942	9.904	19.468
99.969	8.161	15.441
99.988	7.396	20.734
99.996	10.595	23.756
99.999	9.749	15.026
100.000	12.803	14.477
end
0.161	0.034
0.164	0.175
0.167	0.113
0.175	0.110
0.186	0.137
0.202	0.120
0.221	0.123
0.234	0.151
0.250	0.096
0.269	0.172
0.300	0.172
0.354	0.281
0.418	0.528
0.520	0.714
0.697	0.738
0.986	0.741
1.498	0.799
2.280	0.844
3.495	0.851
5.212	0.892
7.671	0.913
10.919	0.933
15.096	0.961
20.252	0.988
26.164	1.015
32.658	1.050
39.589	1.084
46.584	1.132
53.406	1.201
59.904	1.256
65.873	1.352
71.047	1.468
75.638	1.626
79.429	1.825
82.574	2.024
85.195	2.326
87.353	2.580
89.042	2.943
90.460	3.218
91.677	3.430
92.749	3.746
93.684	3.979
94.492	4.171
95.212	4.693
95.861	4.744
96.446	5.111
96.959	5.283
97.406	5.533
97.806	5.907
98.141	6.014
98.462	6.017
98.738	6.635
98.976	6.936
99.225	7.527
99.412	8.178
99.564	7.856
99.686	7.815
99.780	9.111
99.858	9.372
99.913	11.135
99.942	11.293
99.969	11.499
99.988	9.564
99.996	16.689
99.999	10.717
100.000	13.640
end
