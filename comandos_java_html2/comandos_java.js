/*Fastp*/
window.Plotly || document.write('<script src="https://cdn.plot.ly/plotly-1.2.0.min.js"><\/script>')

function showOrHide(divname) {
    div = document.getElementById(divname);
    if(div.style.display == 'none')
        div.style.display = 'block';
    else
        div.style.display = 'none';
}

/*VEP*/
document.write('<script type="text/javascript" src="http://www.google.com/jsapi"></script>')
document.write('<script type="text/javascript">google.load("visualization", "1", {packages: ["corechart","table"]});</script>')
document.write('<script type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/charts/51/loader.js"></script>')
document.write('<link id="load-css-0" rel="stylesheet" type="text/css" href="https://www.gstatic.com/charts/51/css/core/tooltip.css">')
document.write('<link id="load-css-1" rel="stylesheet" type="text/css" href="https://www.gstatic.com/charts/51/css/util/util.css">')
document.write('<link id="load-css-2" rel="stylesheet" type="text/css" href="https://www.gstatic.com/charts/51/css/table/table.css">')
document.write('<link id="load-css-3" rel="stylesheet" type="text/css" href="https://www.gstatic.com/charts/51/css/util/format.css">')
document.write('<script type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/charts/51/js/jsapi_compiled_default_module.js"></script>')
document.write('<script type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/charts/51/js/jsapi_compiled_graphics_module.js"></script>')
document.write('<script type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/charts/51/js/jsapi_compiled_ui_module.js"></script>')
document.write('<script type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/charts/51/js/jsapi_compiled_corechart_module.js"></script>')
document.write('<script type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/charts/51/js/jsapi_compiled_table_module.js"></script>')

function init() {
    // charts
    var var_class_pie = drawPie('var_class_pie', 'Variant classes', google.visualization.arrayToDataTable([['Variant class','Count'],['indel',1],['insertion',3],['deletion',5],['substitution',20],['SNV',122]]), null);
var var_class_table = drawTable('var_class_table', 'Variant classes', google.visualization.arrayToDataTable([['Variant class','Count'],['indel',1],['insertion',3],['deletion',5],['substitution',20],['SNV',122]]));

        google.visualization.events.addListener(var_class_pie, 'select', function() {
          var_class_table.setSelection(var_class_pie.getSelection());
        });
        google.visualization.events.addListener(var_class_table, 'select', function() {
          var_class_pie.setSelection(var_class_table.getSelection());
        });
      var var_cons_pie = drawPie('var_cons_pie', 'Consequences (most severe)', google.visualization.arrayToDataTable([['Consequence type','Count'],['frameshift_variant',3],['missense_variant',33],['splice_donor_5th_base_variant',1],['splice_region_variant',5],['splice_polypyrimidine_tract_variant',1],['synonymous_variant',29],['5_prime_UTR_variant',2],['3_prime_UTR_variant',1],['non_coding_transcript_exon_variant',4],['intron_variant',47],['upstream_gene_variant',2],['downstream_gene_variant',4],['intergenic_variant',19]]), {slices: [{color: "#ff69b4"}, {color: "#ffd700"}, {}, {color: "#ff7f50"}, {}, {color: "#76ee00"}, {}, {}, {}, {color: "#02599c"}, {color: "#a2b5cd"}, {color: "#a2b5cd"}, {color: "gray"}]});
var var_cons_table = drawTable('var_cons_table', 'Consequences (most severe)', google.visualization.arrayToDataTable([['Consequence type','Count'],['frameshift_variant',3],['missense_variant',33],['splice_donor_5th_base_variant',1],['splice_region_variant',5],['splice_polypyrimidine_tract_variant',1],['synonymous_variant',29],['5_prime_UTR_variant',2],['3_prime_UTR_variant',1],['non_coding_transcript_exon_variant',4],['intron_variant',47],['upstream_gene_variant',2],['downstream_gene_variant',4],['intergenic_variant',19]]));

        google.visualization.events.addListener(var_cons_pie, 'select', function() {
          var_cons_table.setSelection(var_cons_pie.getSelection());
        });
        google.visualization.events.addListener(var_cons_table, 'select', function() {
          var_cons_pie.setSelection(var_cons_table.getSelection());
        });
      var consequences_pie = drawPie('consequences_pie', 'Consequences (all)', google.visualization.arrayToDataTable([['Consequence type','Count'],['frameshift_variant',10],['missense_variant',82],['splice_donor_5th_base_variant',8],['splice_region_variant',14],['splice_polypyrimidine_tract_variant',5],['synonymous_variant',108],['5_prime_UTR_variant',9],['3_prime_UTR_variant',4],['non_coding_transcript_exon_variant',110],['intron_variant',319],['NMD_transcript_variant',7],['non_coding_transcript_variant',52],['upstream_gene_variant',213],['downstream_gene_variant',172],['intergenic_variant',19]]), {slices: [{color: "#ff69b4"}, {color: "#ffd700"}, {}, {color: "#ff7f50"}, {}, {color: "#76ee00"}, {}, {}, {}, {color: "#02599c"}, {}, {}, {color: "#a2b5cd"}, {color: "#a2b5cd"}, {color: "gray"}]});
var consequences_table = drawTable('consequences_table', 'Consequences (all)', google.visualization.arrayToDataTable([['Consequence type','Count'],['frameshift_variant',10],['missense_variant',82],['splice_donor_5th_base_variant',8],['splice_region_variant',14],['splice_polypyrimidine_tract_variant',5],['synonymous_variant',108],['5_prime_UTR_variant',9],['3_prime_UTR_variant',4],['non_coding_transcript_exon_variant',110],['intron_variant',319],['NMD_transcript_variant',7],['non_coding_transcript_variant',52],['upstream_gene_variant',213],['downstream_gene_variant',172],['intergenic_variant',19]]));

        google.visualization.events.addListener(consequences_pie, 'select', function() {
          consequences_table.setSelection(consequences_pie.getSelection());
        });
        google.visualization.events.addListener(consequences_table, 'select', function() {
          consequences_pie.setSelection(consequences_table.getSelection());
        });
      var coding_pie = drawPie('coding_pie', 'Coding consequences', google.visualization.arrayToDataTable([['Consequence type','Count'],['frameshift_variant',10],['missense_variant',82],['synonymous_variant',108]]), {slices: [{color: "#ff69b4"}, {color: "#ffd700"}, {color: "#76ee00"}]});
var coding_table = drawTable('coding_table', 'Coding consequences', google.visualization.arrayToDataTable([['Consequence type','Count'],['frameshift_variant',10],['missense_variant',82],['synonymous_variant',108]]));

        google.visualization.events.addListener(coding_pie, 'select', function() {
          coding_table.setSelection(coding_pie.getSelection());
        });
        google.visualization.events.addListener(coding_table, 'select', function() {
          coding_pie.setSelection(coding_table.getSelection());
        });
      var sift_pie = drawPie('sift_pie', 'SIFT summary', google.visualization.arrayToDataTable([['Prediction','Count'],['tolerated_low_confidence',4],['deleterious_low_confidence',11],['deleterious',21],['tolerated',30]]), {slices: [{}, {}, {color: "red"}, {color: "green"}]});
var sift_table = drawTable('sift_table', 'SIFT summary', google.visualization.arrayToDataTable([['Prediction','Count'],['tolerated_low_confidence',4],['deleterious_low_confidence',11],['deleterious',21],['tolerated',30]]));

        google.visualization.events.addListener(sift_pie, 'select', function() {
          sift_table.setSelection(sift_pie.getSelection());
        });
        google.visualization.events.addListener(sift_table, 'select', function() {
          sift_pie.setSelection(sift_table.getSelection());
        });
      var polyphen_pie = drawPie('polyphen_pie', 'PolyPhen summary', google.visualization.arrayToDataTable([['Prediction','Count'],['possibly_damaging',14],['probably_damaging',17],['benign',36]]), {slices: [{}, {}, {color: "green"}]});
var polyphen_table = drawTable('polyphen_table', 'PolyPhen summary', google.visualization.arrayToDataTable([['Prediction','Count'],['possibly_damaging',14],['probably_damaging',17],['benign',36]]));

        google.visualization.events.addListener(polyphen_pie, 'select', function() {
          polyphen_table.setSelection(polyphen_pie.getSelection());
        });
        google.visualization.events.addListener(polyphen_table, 'select', function() {
          polyphen_pie.setSelection(polyphen_table.getSelection());
        });
      var chr_bar = drawBar('chr_bar', 'Variants by chromosome', google.visualization.arrayToDataTable([['Chromosome','Count'],['19',151]]), {legend: {position: "none"}});
var chr_table = drawTable('chr_table', 'Variants by chromosome', google.visualization.arrayToDataTable([['Chromosome','Count'],['19',151]]));

        google.visualization.events.addListener(chr_bar, 'select', function() {
          chr_table.setSelection(chr_bar.getSelection());
        });
        google.visualization.events.addListener(chr_table, 'select', function() {
          chr_bar.setSelection(chr_table.getSelection());
        });
      var chr_19_area = drawArea('chr_19_area', 'Distribution of variants on chromosome 19', google.visualization.arrayToDataTable([['Position (mb)','Count'],['0',0],['1',1],['2',0],['3',55],['4',0],['5',0],['6',19],['7',0],['8',0],['9',2],['10',0],['11',21],['12',5],['13',0],['14',0],['15',1],['16',0],['17',0],['18',0],['19',0],['20',0],['21',0],['22',0],['23',0],['24',2],['25',0],['26',0],['27',14],['28',0],['29',0],['30',0],['31',0],['32',2],['33',0],['34',0],['35',0],['36',0],['37',0],['38',0],['39',0],['40',0],['41',1],['42',0],['43',0],['44',3],['45',1],['46',0],['47',7],['48',1],['49',0],['50',0],['51',0],['52',0],['53',0],['54',14],['55',0],['56',0],['57',0],['58',0],['59',2]]), {hAxis: {title: "Position (mb)", textStyle: {fontSize: 8}}, legend: {position: "none"}});
var protein_bar = drawBar('protein_bar', 'Position in protein', google.visualization.arrayToDataTable([['Position in protein (percentile)','Count'],['00-10%',20],['10-20%',7],['20-30%',9],['30-40%',48],['40-50%',29],['50-60%',13],['60-70%',14],['70-80%',28],['80-90%',21],['90-100%',11]]), {hAxis: {title: "Position in protein (percentile)", textStyle: {fontSize: 10}}, legend: {position: "none"}});

  }
  
  function drawPie(id, title, data, options) {    
    var pie = new google.visualization.PieChart(document.getElementById(id));
    pie.draw(data, options);
    return pie;
  }
  function drawBar(id, title, data, options) {
    var bar = new google.visualization.ColumnChart(document.getElementById(id));
    bar.draw(data, options);
    return bar;
  }
  function drawTable(id, title, data) {
    var table = new google.visualization.Table(document.getElementById(id));
    table.draw(data, null);
    return table;
  }
  function drawLine(id, title, data, options) {
    var line = new google.visualization.LineChart(document.getElementById(id));
    line.draw(data, options);
    return line;
  }
  function drawArea(id, title, data, options) {
    var area = new google.visualization.AreaChart(document.getElementById(id));
    area.draw(data, options);
    return area;
  }
  google.setOnLoadCallback(init);

