
from shiny import App, reactive, render, ui
from faicons import icon_svg
import tempfile
import subprocess
import os
from pathlib import Path
import zipfile
import glob
import base64
import pandas as pd
from io import StringIO

################################# Definición de todos los apartados y su apariencia (ui) #################################
Inicio = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box(
            "¡Bienvenido/a!",
            ui.output_ui("texto_introduccion"),
            showcase=icon_svg("dna"),
        ),
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "1r archivo de lecturas",
            ui.output_text("archivo1_nombre"),
            height="150px",
            showcase=icon_svg("file"),
        ),
        ui.value_box(
            "2o archivo de lecturas",
            ui.output_text("archivo2_nombre"),
            height="150px",
            showcase=icon_svg("file"),
        ),
        ui.value_box(
            "Genoma de referencia",
            ui.output_text("archivo3_nombre"),
            height="150px",
            showcase=icon_svg("book"),
        ),
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Cargue el primer archivo de lecturas",
            ui.input_file("archivo1", "", multiple=False, accept=[".fastq.gz", ".fq.gz"], 
                          button_label="Cargar...", placeholder="Vacío"),
            height="150px",
            showcase=icon_svg("upload"),
        ),
        ui.value_box(
            "Cargue el segundo archivo de lecturas",
            ui.input_file("archivo2", "", multiple=False, accept=[".fastq.gz", ".fq.gz"], 
                          button_label="Cargar...", placeholder="Vacío"),
            showcase=icon_svg("upload"),
        ),
        ui.value_box(
            "Cargue el genoma de referencia para el mapeo",
            ui.input_file("archivo3", "", multiple=False, accept=[".fasta", ".fa"], 
                          button_label="Cargar...", placeholder="Vacío"),
            showcase=icon_svg("upload"),
        ),
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_empezar", "EMPEZAR", disabled=True),
    ),
)

Control_calidad = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box(
            "Comando que se ejecutará:",
            ui.output_text("comando1"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_analisis_calidad", "Iniciar análisis de calidad de las lecturas", disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados del análisis de calidad del 1r archivo de lecturas:",
          ui.output_ui("html1_calidad"),
          showcase=icon_svg("scroll"),
          full_screen=True,
        ),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados del análisis de calidad del 2o archivo de lecturas:",
          ui.output_ui("html2_calidad"),
          showcase=icon_svg("scroll"),
          full_screen=True,
        ),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados1", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente1", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Limpieza_lecturas = ui.page_fluid(
    ui.layout_columns(
        ui.card(ui.value_box(
            "Este apartado es OPCIONAL aunque altamente recomendable",
            ui.output_ui("Opcional_limpieza"),
            showcase=icon_svg("circle-exclamation"),
            ),
            ui.layout_columns(ui.input_action_button("boton_siguiente2a", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
            ),
        ),
    ),
    ui.layout_columns(
        ui.card("Seleccione sus preferencias para la limpieza de las lecturas:",
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_Q_media", "Restringir la calidad de los extremos de las lecturas", True),
                        ui.input_numeric("Q_media", "Eliminar las bases de los extremos que tengan una calidad menor que:", 30, min=1, width="100%")),
                ui.card(ui.input_checkbox("check_Q_inicio", "Recortar bases en el extremo 5' (inicio) de las lecturas", True),
                        ui.input_numeric("Q_inicio", "Número de bases a eliminar al inicio:",
                                          15, min=1, width="100%")),
                ui.card(ui.input_checkbox("check_Q_final", "Recortar bases en el extremo 3' (final) de las lecturas", True),
                        ui.input_numeric("Q_final", "Número de bases a eliminar al final:",
                                          15, min=1, width="100%")),
                ui.card(ui.input_checkbox("check_longitud", "Restringir la longitud mínima de las lecturas", True),
                        ui.input_numeric("longitud", "Eliminar lecturas cuya longitud sea menor que:", 100, min=1, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_adaptadores", "Eliminar adapatadores", True),),
                ui.card(ui.input_checkbox("check_polyG", "Eliminar secuencias polyG", True),),
                ui.card(ui.input_checkbox("check_polyX", "Eliminar secuencias polyX", True),),
                ),
                ui.layout_columns(
                ui.card(ui.input_text("opcion_adicional2", "Si desea añadir alguna opción adicional al comando, escríbala aquí:",
                                       True, width="100%")),
                ),
        ),
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Comando que se ejecutará:",
            ui.output_text("comando2"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_limpieza_lecturas", "Iniciar limpieza de las lecturas", disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados de la limpieza de las lecturas:",
          ui.output_ui("html_limpieza_lecturas"),
          showcase=icon_svg("scroll"),
          full_screen=True,
        ),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados2", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente2", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Indexado = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box(
            "Comando que se ejecutará:",
            ui.output_text("comando3"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_indexado", "Iniciar indexado del genoma de referencia", disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados3", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente3", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Mapeo = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box(
            "Comando que se ejecutará:",
            ui.output_text("comando4"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_mapeo", "Iniciar mapeo de las lecturas contra el genoma de referencia",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados4", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente4", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Analisis_mapeo = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box(
            "Primer comando que se ejecutará para la conversión del archivo SAM a BAM:",
            ui.output_text("comando5b"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Segundo comando que se ejecutará para ordenar el archivo BAM por coordenadas:",
            ui.output_text("comando5c"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Tercer comando que se ejecutará para obtener un informe sobre el resultado del mapeo:",
            ui.output_text("comando5"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Cuarto comando que se ejecutará para graficar el informe sobre el resultado del mapeo:",
            ui.output_text("comando5d"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_analisis_mapeo", "Iniciar analisis del resultado del mapeo",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados del mapeo:",
          ui.output_ui("html_analisis_mapeo"),
          showcase=icon_svg("scroll"),
          full_screen=True,
        ),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados5", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente5", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Limpieza_duplicados = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box(
            "Comando que se ejecutará para marcar los duplicados:",
            ui.output_text("comando6b"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_marcar_duplicados", "Iniciar marcaje de duplicados",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados del marcaje de duplicados:",
          ui.output_ui("txt_Duplicados"),
          showcase=icon_svg("scroll"),
          full_screen=True,
          class_="txt_duplicados",
        ),
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Importante:",
            ui.output_ui("Disclaimer"),
            showcase=icon_svg("triangle-exclamation"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Comando que se ejecutará para comprobar los grupos de lectura (Read Groups) actuales:",
            ui.output_text("comando6c"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_comprobar_ReadGroups", "Iniciar comprobación de Read Groups",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados de la comprobación de los Read Groups:",
          ui.output_ui("txt_ReadGroups"),
          showcase=icon_svg("scroll"),
          full_screen=True,
        ),
    ),
    ui.layout_columns(
        ui.card(
            ui.input_checkbox("check_ReadGroups", 
                            "Si desea añadir Read Groups marque esta casilla, \
                            puede usar los valores predefinidos o introducir los propios", 
                            False, width="100%"),
                ui.layout_columns(
                ui.card(ui.input_text("rgid", "RGID - ID del grupo de lecturas (campo ID):", "default", width="100%")),
                ui.card(ui.input_text("rglibreria", "RGLB - Nombre de la librería (campo LB):", "lib1", width="100%")),
                ui.card(ui.input_text("rgplataforma", "RGPL - Nombre del secuenciador (campo PL):", "NA" , width="100%")),
                ui.card(ui.input_text("rgmuestra", "RGSM - Nombre de la muestra (campo SM):", "sample1", width="100%")),
                ui.card(ui.input_text("rgcarrera", "RGPU - Nombre de la carrera (run) (campo PU):", "unit1", width="100%")),
                ),
                ui.value_box(
                "Comando que se ejecutará para añadir los Read Groups:",
                ui.output_text("comando6d"),
                showcase=icon_svg("terminal"),
            ),
        ),
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_añadir_ReadGroups", "Iniciar adición de Read Groups",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados6", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente6", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Llamada_variantes = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box(
            "Primer comando que se ejecutará para indexar el genoma de referencia:",
            ui.output_text("comando7c"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Segundo comando que se ejecutará para indexar el archivo de mapeo:",
            ui.output_text("comando7d"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card("Puede añadir opciones al comando para la llamada de variantes si lo desea:",
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_ploidia", "Ploidía", False),
                        ui.input_numeric("ploidia", "La ploidia del organismo es de:", 2, min=1, width="100%")),
                ui.card(ui.input_checkbox("check_min_frecuencia", "Fracción mínima", False),
                        ui.input_numeric("min_frecuencia", "La fracción mínima de lecturas que apoyan el alelo alternativo \
                                          para que se considere como una variante debe ser de:",
                                          0.2, min=0.01, width="100%")),
                ui.card(ui.input_checkbox("check_min_lecturas", "Cantidad de lecturas mínima", False),
                        ui.input_numeric("min_lecturas", "La cantidad mínima de lecturas que apoyan el alelo alternativo\
                                          para que se considere como una variante debe ser de:",
                                          50, min=1, width="100%")),
                ui.card(ui.input_checkbox("check_min_calidad_mapeo", "Calidad de mapeo mínima", False),
                        ui.input_numeric("min_calidad_mapeo", "La calidad mínima de mapeo de una lectura necesaria para \
                                         considerarla en la llamada variantes debe ser de:", 20, min=1, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_text("opcion_adicional7e", "Si desea añadir alguna opción adicional al comando, escríbala aquí:",
                                       True, width="100%")),
                ),
                ui.value_box(
                "Tercer comando que se ejecutará para hacer la llamada de variantes:",
                ui.output_text("comando7e"),
                showcase=icon_svg("terminal"),
            ),
        ),
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Cuarto comando que se ejecutará para obtener un informe de la llamada de variantes:",
            ui.output_text("comando7f"),
            showcase=icon_svg("terminal"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_llamada_variantes", "Iniciar llamada de variantes",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados de la llamada de variantes:",
          ui.output_ui("txt_llamada_variantes"),
          showcase=icon_svg("scroll"),
          full_screen=True,
          class_="txt_llamada_variantes",
        ),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados7", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente7", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Filtrado_variantes = ui.page_fluid(
    ui.layout_columns(
        ui.card(ui.value_box(
            "Este apartado es OPCIONAL",
            ui.output_ui("Opcional"),
            showcase=icon_svg("circle-exclamation"),
            ),
            ui.layout_columns(ui.input_action_button("boton_siguiente8a", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
            ),
        ),
    ),
    ui.layout_columns(
        ui.card("Si desea filtrar las variantes, puede seleccionar alguna de estas opciones o añadir una propia:",
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_calidad_variantes", "Filtrar por calidad mínima", False),
                        ui.input_numeric("calidad_variantes", "Eliminar variantes cuya calidad sea menor que:",
                                          30, min=1, width="100%")),
                ui.card(ui.input_checkbox("check_profundidad_min", "Filtrar por profundidad mínima", False),
                        ui.input_numeric("profundidad_min", "Eliminar variantes cuya profundidad de cobertura sea menor que:",
                                          10, min=1, width="100%")),
                ui.card(ui.input_checkbox("check_profundidad_max", "Filtrar por profundidad máxima", False),
                        ui.input_numeric("profundidad_max", "Eliminar variantes cuya profundidad de cobertura sea mayor que:",
                                          100, min=1, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_eliminar_indels", "Eliminar los indels", False)),
                ui.card(ui.input_checkbox("check_mantener_indels", "Mantener únicamente los indels", False)),
                ),
                ui.layout_columns(
                ui.card(ui.input_text("opcion_adicional8", "Si desea añadir alguna opción adicional al comando, escríbala aquí:",
                                       True, width="100%")),
                ),
                ui.value_box(
                "Primer comando que se ejecutará para hacer el filtrado de variantes:",
                ui.output_text("comando8"),
                showcase=icon_svg("terminal"),
                ),
                ui.value_box(
                "Segundo comando que se ejecutará para obtener un informe del filtrado de variantes:",
                ui.output_text("comando8d"),
                showcase=icon_svg("terminal"),
            ),
        ),
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_filtrado_variantes", "Iniciar filtrado de variantes",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados del filtrado de variantes:",
          ui.output_ui("txt_filtrado_variantes"),
          showcase=icon_svg("scroll"),
          full_screen=True,
          class_="txt_llamada_variantes",
        ),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados8", "Descargar resultados", disabled=True, icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente8b", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Efecto_variantes = ui.page_fluid(
    ui.layout_columns(
        ui.card("Seleccione sus preferencias para la predicción del efecto de las variantes:",
                ui.layout_columns(
                ui.card(ui.tooltip(ui.input_checkbox("check_assembly", "Ensamblado del genoma:", True),
                                    "Si no se indica, VEP tratará de inferirlo. Si no lo consigue, asumirá el GRCh38.", 
                                    id="tooltip_assembly", placement="right"),
                                    ui.input_select("seleccion_assembly", "", {"GRCh37": "GRCh37", "GRCh38": "GRCh38"},
                                                    selected="GRCh37", width="100%")),
                ui.card(ui.tooltip(ui.input_checkbox("check_clin_sig_allele", "Obtener significancia clínica:", False),
                                   'En función de la posición genómica: Devuelve toda la información de \
                                    significancia clínica conocida para la posición genómica de la variante, independientemente del alelo. \
                                    En función del alelo: Devuelve solo la información de significancia \
                                    clínica conocida para el alelo en el que se encuentra la variante',
                                    id="tooltip_clin_sig", placement="right"),
                                    ui.input_select("seleccion_clin_sig", "", 
                                                    {"0": "En función de la posición genómica", "1" : "En función del alelo"},
                                                    selected="1", width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.tooltip(ui.input_checkbox("check_sift", "Calcular SIFT", False),
                                   'Clasificación: Asigna una categoria a la variante en función de la predicción \
                                    (ej. "Tolerada" o "Dañina"). Puntuación: muestra la puntuación entre 0 y 1, siendo cercano a 0 \
                                    "probablemente dañina" y cercano a 1 "probablemente tolerada".',
                                    id="tooltip_sift", placement="right"),
                                    ui.input_select("seleccion_sift", "", 
                                                    {"p": "Clasificación", "s" : "Puntuación", "b": "Clasificación + puntuación"},
                                                    selected="b", width="100%")),
                ui.card(ui.tooltip(ui.input_checkbox("check_polyphen", "Calcular PolyPhen", False),
                                   'Clasificación: Asigna una categoria a la variante en función de la predicción \
                                    (ej. "Benigna" o "Dañina"). Puntuación: muestra la puntuación entre 0 y 1, siendo cercano a 0 \
                                    "probablemente benigna" y cercano a 1 "probablemente dañina".',
                                    id="tooltip_polyphen", placement="right"),
                                    ui.input_select("seleccion_polyphen", "", 
                                                    {"p": "Clasificación", "s" : "Puntuación", "b": "Clasificación + Puntuación"},
                                                    selected="b", width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_gene_phenotype", "Obtener fenotipos asociados al gen afectado", 
                                          False, width="100%")),
                ui.card(ui.input_checkbox("check_variant_class", "Obtener la clase de variante (Sequence Ontology)", False, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_symbol", "Obtener símbolo del gen afectado", False, width="100%")),
                ui.card(ui.input_checkbox("check_protein", "Obtener el identificador Ensembl de la proteína", False, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_hgvs", "Obtener nomenclatura HGVS de la variante", False, width="100%")),
                ui.card(ui.input_checkbox("check_spdi", "Obtener nomenclatura SPDI de la variante", False, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_check_existing", "Obtener datos de variantes conocidas colocalizadas", False, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_uniprot", "Obtener referencias UniProt de proteínas colocalizadas", False, width="100%")),
                ),
                ui.layout_columns(
                ui.card(ui.input_checkbox("check_af", "Obtener frecuencia alélica global de variantes colocalizadas", False, width="100%")),
                ),
                ui.layout_columns(
                    ui.input_checkbox("check_fields", "Limitar y ordenar los campos a incluir en la tabla:",
                                       False, width="100%"),
                        ui.input_selectize("campos_seleccionados", "",
                                            ("Uploaded_variation","Location","Allele","Gene","Feature","Feature_type","Consequence",
                                            "cDNA_position","CDS_position","Protein_position","Amino_acids","Codons","Existing_variation",
                                            "VARIANT_CLASS","SIFT","PolyPhen","NEAREST","GENE_PHENO","MOTIF_NAME","MOTIF_POS","HIGH_INF_POS",
                                            "MOTIF_SCORE_CHANGE","CELL_TYPE","IND","ZYG","ALLELE_NUM","REF_ALLELE","UPLOADED_ALLELE",
                                            "EXON","INTRON","HGVSc","HGVSp","HGVS_OFFSET","HGVSg","SPDI","ENSP","SYMBOL","SYMBOL_SOURCE",
                                            "HGNC_ID","CCDS","SWISSPROT","TREMBL","UNIPARC","UNIPROT_ISOFORM","TSL","APPRIS","CANONICAL",
                                            "MANE_SELECT","MANE_PLUS_CLINICAL","BIOTYPE","DOMAINS","RefSeq","CLIN_SIG","SOMATIC","PHENO",
                                            "SV","AF","CHECK_REF", "PICK","FREQS"),
                                            multiple=True, width="100%"),
                ),
                ui.layout_columns(
                ui.card(ui.input_text("opcion_adicional9", "Si desea añadir alguna opción adicional al comando, escríbala aquí:",
                                       True, width="100%")),
                ),
                ui.value_box(
                "Comando que se ejecutará para predecir el efecto de las variantes:",
                ui.output_text("comando9"),
                showcase=icon_svg("terminal"),
            ),
        ),
    ),
    ui.layout_column_wrap(
        ui.input_action_button("boton_VEP", "Iniciar predicción del efecto de las variantes",
                                disabled=True, icon=icon_svg("circle-play")),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados generales de la predicción del efecto de las variantes:",
          ui.output_ui("html_VEP"),
          showcase=icon_svg("scroll"),
          full_screen=True,
        ),
    ),
    ui.layout_column_wrap(
        ui.value_box(
          "Informe de resultados tabulados de la predicción del efecto de las variantes:",
          ui.output_ui("tabla_VEP"),
          showcase=icon_svg("scroll"),
          full_screen=True,
        ),
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_resultados9", "Descargar resultados", icon=icon_svg("download")),
        ui.input_action_button("boton_siguiente9", "Siguiente", disabled=True, icon=icon_svg("circle-right")),
    ),
)

Resumen = ui.page_fluid(
    ui.layout_column_wrap(
        ui.value_box("",
            ui.output_ui("texto_resumen"),
            showcase=icon_svg("dna"),
        ),
    ),
    ui.accordion(
        ui.accordion_panel("Resumen de los comandos ejecutados:",
            ui.layout_column_wrap(
                ui.card(
                    ui.card("1. Control de calidad",
                        ui.value_box(
                        "Obtener un informe de la calidad de las lecturas:",
                        ui.output_ui("calidad_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("2. Limpieza de lecturas:",
                        ui.value_box(
                        "Realizar la limpieza de las lecturas:",
                        ui.output_ui("limpieza_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("3. Indexado del genoma de referencia:",
                        ui.value_box(
                        "Indexar el genoma de referencia:",
                        ui.output_ui("indexado_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("4. Mapeo:",
                        ui.value_box(
                        "Mapear las lecturas contra el genoma de referencia:",
                        ui.output_ui("mapeo_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("5. Análisis del mapeo:",
                        ui.value_box(
                        "Convertir el archivo SAM a BAM:",
                        ui.output_ui("analisis_mapeo1_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Ordenar el archivo BAM por coordenadas:",
                        ui.output_ui("analisis_mapeo2_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Obtener informe del resultado del mapeo:",
                        ui.output_ui("analisis_mapeo3_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Graficar el informe del resultado del mapeo:",
                        ui.output_ui("analisis_mapeo4_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("6. Limpieza de duplicados:",
                        ui.value_box(
                        "Marcar los duplicados:",
                        ui.output_ui("limpieza_duplicados1_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Observar los Read Groups:",
                        ui.output_ui("limpieza_duplicados2_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Añadir o reemplazar los Read Groups:",
                        ui.output_ui("limpieza_duplicados3_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("7. Llamada de variantes:",
                        ui.value_box(
                        "Indexar el genoma de referencia:",
                        ui.output_ui("llamada_variantes1_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Indexar el archivo de mapeo:",
                        ui.output_ui("llamada_variantes2_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Realizar la llamada de variantes:",
                        ui.output_ui("llamada_variantes3_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Obtener un informe de estadísticas de la llamada de variantes:",
                        ui.output_ui("llamada_variantes4_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("8. Filtrado de variantes:",
                        ui.value_box(
                        "Filtrar las variantes:",
                        ui.output_ui("filtrado_variantes1_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                        ui.value_box(
                        "Obtener un informe de estadísticas del filtrado de variantes:",
                        ui.output_ui("filtrado_variantes2_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                    ui.card("9. Predicción del efecto de las variantes:",
                        ui.value_box(
                        "Predecir el efecto de las variantes:",
                        ui.output_ui("efecto_variantes_rc"),
                        showcase=icon_svg("terminal"),
                        ),
                    ),
                ),
            ),
        ),
        ui.accordion_panel("Script con los comandos ejecutados:",
            ui.layout_column_wrap(
                ui.value_box(
                "",
                ui.output_ui("script"),
                full_screen=True,
                height="150px",
                ),
            ),
            ui.layout_column_wrap(
                ui.download_button("descarga_script_sh", "Descargar script (.sh)", disabled=False, icon=icon_svg("download")),
                ui.download_button("descarga_script_txt", "Descargar script (.txt)", disabled=False, icon=icon_svg("download")),
            ),
        ),
        ui.accordion_panel("Resumen de resultados:",
            ui.layout_column_wrap(
                ui.card(
                    ui.card("Control de calidad:",
                        ui.value_box(
                        "Del 1r archivo de lecturas:",
                        ui.output_ui("calidad_1_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        ),
                        ui.value_box(
                        "Del 2o archivo de lecturas:",
                        ui.output_ui("calidad_2_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        ),
                    ),
                    ui.card("Limpieza de lecturas:",
                        ui.value_box(
                        "",
                        ui.output_ui("limpieza_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        ),
                    ),
                    ui.card("Mapeo:",
                        ui.value_box(
                        "",
                        ui.output_ui("analisis_mapeo_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        ),
                    ),
                    ui.card("Marcaje de duplicados:",
                        ui.value_box(
                        "",
                        ui.output_ui("duplicados_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        class_="txt_duplicados",
                        ),
                    ),
                    ui.card("Read Groups:",
                        ui.value_box(
                        "",
                        ui.output_ui("RG_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        ),
                    ),
                    ui.card("Llamada de variantes:",
                        ui.value_box(
                        "",
                        ui.output_ui("llamada_variantes_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        class_="txt_llamada_variantes",
                        ),
                    ),
                    ui.card("Filtrado de variantes:",
                        ui.value_box(
                        "",
                        ui.output_ui("filtrado_variantes_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        class_="txt_llamada_variantes",
                        ),
                    ),
                    ui.card("Efecto de las variantes:",
                        ui.value_box(
                        "Resumen general:",
                        ui.output_ui("efecto_variantes_general_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        ),
                        ui.value_box(
                        "Tabla de variantes:",
                        ui.output_ui("efecto_variantes_tabla_rr"),
                        showcase=icon_svg("scroll"),
                        full_screen=True,
                        ),
                    ),
                ),
            ),
        ),
    open=False, multiple=True
    ),
    ui.layout_column_wrap(
        ui.download_button("descarga_todos_archivos", "Descargar todos los archivos generados", disabled=False, icon=icon_svg("download")),
    ),
    )

# Definición de la barra lateral del programa (donde están los apartados definidos previamente)
app_ui = ui.page_fluid(
    ui.head_content(ui.include_css("./custom_css/custom.css"),
                    ui.include_css("./comando_css_html2/comando_css.css"),
                    ui.include_js("./comandos_java_html2/comandos_java.js")
                    ),
    ui.panel_title("GenAgans", "GenAgans"),
    ui.navset_pill_list(
       ui.nav_panel("Inicio", Inicio, icon=icon_svg("dna")),
       ui.nav_panel("1. Control de calidad de las lecturas", Control_calidad),
       ui.nav_panel("2. Limpieza de las lecturas", Limpieza_lecturas),
       ui.nav_panel("3. Indexado del genoma de referencia", Indexado),
       ui.nav_panel("4. Mapeo", Mapeo),
       ui.nav_panel("5. Análisis del mapeo", Analisis_mapeo),
       ui.nav_panel("6. Limpieza de duplicados", Limpieza_duplicados),
       ui.nav_panel("7. Llamada de variantes", Llamada_variantes),
       ui.nav_panel("8. Filtrado de variantes", Filtrado_variantes),
       ui.nav_panel("9. Efecto de las variantes", Efecto_variantes),
       ui.nav_panel("Resumen", Resumen, icon=icon_svg("dna")),
       widths=(2,10),
       id="panel",
    ),
)


# Creación de una careta temporal y definición de la carpeta de trabajo (working directory)
dir_temp = tempfile.mkdtemp(prefix="GenAgans")
ruta_archivos = f"{Path(dir_temp)}"
os.chdir(ruta_archivos)


################################# Definición del servidor: todos los efectos reactivos #################################
def server(input, output, session):

#################### Variables globales de definición reactiva ####################
##### Inicio - Nombres archivos #####
    nombre_archivo1_completo = reactive.Value("")
    nombre_archivo2_completo = reactive.Value("")
    nombre_archivo3_completo = reactive.Value("")
    nombre_archivo1_sin_extensiones = reactive.Value("")
    nombre_archivo2_sin_extensiones = reactive.Value("")

##### 1. Analisis calidad #####
    comando1_a_actual = reactive.Value("")
    comando1_actual = reactive.Value("")
    analisis_calidad_completado = reactive.Value(False)
    resultado_html1_calidad = reactive.Value("Todavía no hay resultados")
    resultado_html2_calidad = reactive.Value("Todavía no hay resultados")
    comando1a_ejecutado = reactive.Value("")
    comando1_ejecutado = reactive.Value("")

##### 2. Limpieza lecturas #####
    comando2_a_actual = reactive.Value("")
    comando2_b1_actual = reactive.Value("")
    comando2_b2_actual = reactive.Value("")
    comando2_actual = reactive.Value("")
    limpieza_lecturas_completado = reactive.Value(False)
    salto_apartado2 = reactive.Value(False)
    resultado_html_limpieza_lecturas = reactive.Value("Todavía no hay resultados")
    comando2a_ejecutado = reactive.Value("")
    comando2b1_ejecutado = reactive.Value("")
    comando2b2_ejecutado = reactive.Value("")
    comando2_ejecutado = reactive.Value("")
## Opciones comando 2 - Limpieza lecturas ##
    cut_tail = reactive.Value("")
    cut_tail_num = reactive.Value("")
    cut_front = reactive.Value("")
    cut_front_num = reactive.Value("")
    cut_mean_quality = reactive.Value("")
    cut_mean_quality_num = reactive.Value("")
    detect_adapter_for_pe = reactive.Value("")
    trim_poly_g = reactive.Value("")
    trim_poly_x = reactive.Value("")
    longitud_l = reactive.Value("")
    longitud_num = reactive.Value("")
    opcion_adicional_2 = reactive.Value("")

##### 3. Indexado del genoma de referencia #####
    comando3_a_actual = reactive.Value("")
    comando3_b_actual = reactive.Value("")
    comando3_actual = reactive.Value("")
    indexado_completado = reactive.Value(False)
    comando3a_ejecutado = reactive.Value("")
    comando3b_ejecutado = reactive.Value("")
    comando3_ejecutado = reactive.Value("")

##### 4. Mapeo #####
    comando4_a_actual = reactive.Value("")
    comando4_actual = reactive.Value("")
    mapeo_completado = reactive.Value(False)
    comando4a_ejecutado = reactive.Value("")
    comando4_ejecutado = reactive.Value("")

##### 5. Análisis del mapeo #####
    comando5_a_actual = reactive.Value("")
    comando5_b_actual = reactive.Value("")
    comando5_c_actual = reactive.Value("")
    comando5_actual = reactive.Value("")
    comando5_d_actual = reactive.Value("")
    analisis_mapeo_completado = reactive.Value(False)
    resultado_html_analisis_mapeo = reactive.Value("Todavía no hay resultados")
    comando5a_ejecutado = reactive.Value("")
    comando5b_ejecutado = reactive.Value("")
    comando5c_ejecutado = reactive.Value("")
    comando5_ejecutado = reactive.Value("")
    comando5d_ejecutado = reactive.Value("")

##### 6. Limpieza de duplicados #####
    comando6_a_actual = reactive.Value("")
    comando6_b_actual = reactive.Value("")
    comando6_c_actual = reactive.Value("")
    comando6_d0_actual = reactive.Value("")
    comando6_d_actual = reactive.Value("")
    comando6_b_completado = reactive.Value(False)
    comando6_c_completado = reactive.Value(False)
    resultado_txt_Duplicados = reactive.Value("Todavía no hay resultados")
    resultado_txt_ReadGroups = reactive.Value("Todavía no hay resultados")
    comando6a_ejecutado = reactive.Value("")
    comando6b_ejecutado = reactive.Value("")
    comando6c_ejecutado = reactive.Value("")
    comando6d0_ejecutado = reactive.Value("")
    comando6d_ejecutado = reactive.Value("")
## Opciones comando 6d ##
    RGID = reactive.Value("")
    RGLB = reactive.Value("")
    RGPL = reactive.Value("")
    RGSM = reactive.Value("")
    RGPU = reactive.Value("")
    
##### 7. Llamada de variantes #####
    comando7_a_actual = reactive.Value("")
    comando7_b_actual = reactive.Value("")
    comando7_c_actual = reactive.Value("")
    comando7_d_actual = reactive.Value("")
    comando7_e_actual = reactive.Value("")
    comando7_f_actual = reactive.Value("")
    llamada_variantes_completado = reactive.Value(False)
    resultado_txt_llamada_variantes = reactive.Value("Todavía no hay resultados")
    comando7a_ejecutado = reactive.Value("")
    comando7b_ejecutado = reactive.Value("")
    comando7c_ejecutado = reactive.Value("")
    comando7d_ejecutado = reactive.Value("")
    comando7e_ejecutado = reactive.Value("")
    comando7f_ejecutado = reactive.Value("")
## Opciones comando 7e ##
    ploidy = reactive.Value("")
    ploidy_num = reactive.Value("")
    min_alternate_fraction = reactive.Value("")
    min_alternate_fraction_num = reactive.Value("")
    min_alternate_count = reactive.Value("")
    min_alternate_count_num = reactive.Value("")
    min_mapping_quality = reactive.Value("")
    min_mapping_quality_num = reactive.Value("")
    opcion_adicional_7e = reactive.Value("")

##### 8. Filtrado de variantes #####
    comando8_a_actual = reactive.Value("")
    comando8_b0_actual = reactive.Value("")
    comando8_b_actual = reactive.Value("")
    comando8_actual = reactive.Value("")
    comando8_c_actual = reactive.Value("")
    comando8_d_actual = reactive.Value("")
    filtrado_variantes_completado = reactive.Value(False)
    salto_apartado8 = reactive.Value(False)
    resultado_txt_filtrado_variantes = reactive.Value("Todavía no hay resultados")
    comando8a_ejecutado = reactive.Value("")
    comando8b0_ejecutado = reactive.Value("")
    comando8b_ejecutado = reactive.Value("")
    comando8_ejecutado = reactive.Value("")
    comando8c_ejecutado = reactive.Value("")
    comando8d_ejecutado = reactive.Value("")
## Opciones comando 8 ##
    minQ = reactive.Value("")
    minQ_num = reactive.Value("")
    minDP = reactive.Value("")
    minDP_num = reactive.Value("")
    maxDP = reactive.Value("")
    maxDP_num = reactive.Value("")
    remove_indels = reactive.Value("")
    keep_only_indels = reactive.Value("")
    opcion_adicional_8 = reactive.Value("")

##### 9. Efecto de las variantes #####
    comando9_a_actual = reactive.Value("")
    comando9_actual = reactive.Value("")
    efecto_variantes_completado = reactive.Value(False)
    resultado_html_VEP = reactive.Value("Todavía no hay resultados")
    resultado_tabla_VEP = reactive.Value("Todavía no hay resultados")
    comando9a_ejecutado = reactive.Value("")
    comando9_ejecutado = reactive.Value("")
## Opciones comando 9 ##
    assembly = reactive.Value("")
    assembly_valor = reactive.Value("")
    clin_sig_allele = reactive.Value("")
    clin_sig_allele_valor = reactive.Value("")
    sift = reactive.Value("")
    sift_valor = reactive.Value("")
    polyphen = reactive.Value("")
    polyphen_valor = reactive.Value("")
    gene_phenotype = reactive.Value("")
    variant_class = reactive.Value("")
    symbol = reactive.Value("")
    protein = reactive.Value("")
    hgvs = reactive.Value("")
    spdi = reactive.Value("")
    check_existing = reactive.Value("")
    uniprot = reactive.Value("")
    af = reactive.Value("")
    fields = reactive.Value("")
    fields_valor = reactive.Value("")
    opcion_adicional_9 = reactive.Value("")

##### 10. Resumen #####
    comandos_ejecutados_html = reactive.Value("")
    comandos_ejecutados_sh_txt = reactive.Value("")


#################### Actualización reactiva de los comandos ####################
##### 1. Limpieza Lecturas #####
    @reactive.effect
    def comando1_a_actualizacion():
        comando1_a_actual.set("mkdir 1.Analisis_calidad")

    @reactive.effect
    def comando1_actualizacion():
        comando1_actual.set(f"fastqc -o 1.Analisis_calidad/ {nombre_archivo1_completo.get()} {nombre_archivo2_completo.get()}")

##### 2. Control Calidad #####
    @reactive.effect
    def comando2_a_actualizacion():
        comando2_a_actual.set("mkdir 2.Lecturas_limpias")

    @reactive.effect
    def comando2_b0_actualizacion():
        comando2_b1_actual.set(f"cp {nombre_archivo1_completo.get()} ./2.Lecturas_limpias/{nombre_archivo1_sin_extensiones.get()}_clean.fq.gz")
    
    @reactive.effect
    def comando2_b1_actualizacion():
        comando2_b2_actual.set(f"cp {nombre_archivo2_completo.get()} ./2.Lecturas_limpias/{nombre_archivo2_sin_extensiones.get()}_clean.fq.gz")

    @reactive.effect
    def comando2_actualizacion():
        comando2_actual.set(f"fastp -i {nombre_archivo1_completo.get()} -I {nombre_archivo2_completo.get()} \
                -o ./2.Lecturas_limpias/{nombre_archivo1_sin_extensiones.get()}_clean.fq.gz \
                -O ./2.Lecturas_limpias/{nombre_archivo2_sin_extensiones.get()}_clean.fq.gz \
                {cut_tail.get()} {cut_tail_num.get()} {cut_front.get()} {cut_front_num.get()} {cut_mean_quality.get()} \
                {cut_mean_quality_num.get()} {detect_adapter_for_pe.get()} {trim_poly_g.get()} {trim_poly_x.get()} {longitud_l.get()} \
                {longitud_num.get()} {opcion_adicional_2.get()}\
                -h ./2.Lecturas_limpias/{nombre_archivo1_sin_extensiones.get()}_{nombre_archivo2_sin_extensiones.get()}_fastp.html \
                -j ./2.Lecturas_limpias/{nombre_archivo1_sin_extensiones.get()}_{nombre_archivo2_sin_extensiones.get()}_fastp.json")

##### 3. Indexado del genoma de referencia #####
    @reactive.effect
    def comando3_a_actualizacion():
        comando3_a_actual.set("mkdir 3.Genoma_referencia_indexado")
    
    @reactive.effect
    def comando3_b_actualizacion():
        comando3_b_actual.set(f"cp {nombre_archivo3_completo.get()} ./3.Genoma_referencia_indexado/{nombre_archivo3_completo.get()}")

    @reactive.effect
    def comando3_actualizacion():
        comando3_actual.set(f"bwa index -p ./3.Genoma_referencia_indexado/{nombre_archivo3_completo.get()} \
                            ./3.Genoma_referencia_indexado/{nombre_archivo3_completo.get()}")

##### 4. Mapeo #####
    @reactive.effect
    def comando4_a_actualizacion():
        comando4_a_actual.set("mkdir 4.Mapeo")

    @reactive.effect
    def comando4_actualizacion():
        comando4_actual.set(f"bwa mem -a ./3.Genoma_referencia_indexado/{nombre_archivo3_completo.get()} \
                            ./2.Lecturas_limpias/{nombre_archivo1_sin_extensiones.get()}_clean.fq.gz \
                            ./2.Lecturas_limpias/{nombre_archivo2_sin_extensiones.get()}_clean.fq.gz \
                            -o ./4.Mapeo/mapeo.sam")

##### 5. Análisis del mapeo #####
    @reactive.effect
    def comando5_a_actualizacion():
        comando5_a_actual.set("mkdir 5.Analisis_mapeo")

    @reactive.effect
    def comando5_b_actualizacion():
        comando5_b_actual.set("samtools view -bS ./4.Mapeo/mapeo.sam -o ./5.Analisis_mapeo/mapeo.bam")

    @reactive.effect
    def comando5_c_actualizacion():
        comando5_c_actual.set("samtools sort ./5.Analisis_mapeo/mapeo.bam -o ./5.Analisis_mapeo/mapeo_sorted.bam")
    
    @reactive.effect
    def comando5_actualizacion():
        comando5_actual.set("samtools stats ./5.Analisis_mapeo/mapeo_sorted.bam > ./5.Analisis_mapeo/analisis_mapeo.txt")
    
    @reactive.effect
    def comando5_d_actualizacion():
        comando5_d_actual.set("plot-bamstats -p ./5.Analisis_mapeo/informe_mapeo ./5.Analisis_mapeo/analisis_mapeo.txt")

##### 6. Limpieza de duplicados #####
    @reactive.effect
    def comando6_a_actualizacion():
        comando6_a_actual.set("mkdir 6.Limpieza_duplicados")
    
    @reactive.effect
    def comando6_b_actualizacion():
        comando6_b_actual.set("picard MarkDuplicates --INPUT ./5.Analisis_mapeo/mapeo_sorted.bam \
                              --OUTPUT ./6.Limpieza_duplicados/mapeo_dedup.bam \
                              --METRICS_FILE ./6.Limpieza_duplicados/MarkDuplicatesMetrics.txt \
                              --ASSUME_SORTED True")

    @reactive.effect
    def comando6_c_actualizacion():
        comando6_c_actual.set('samtools view -H ./6.Limpieza_duplicados/mapeo_dedup.bam | grep "^@RG" > ./6.Limpieza_duplicados/ReadGroups.txt')

    @reactive.effect
    def comando7_d0_actualizacion():
        comando6_d0_actual.set("mv ./6.Limpieza_duplicados/mapeo_dedup.bam ./6.Limpieza_duplicados/mapeo_dedup_copy.bam")

    @reactive.effect
    def comando6_d_actualizacion():
        comando6_d_actual.set(f"picard AddOrReplaceReadGroups -I ./6.Limpieza_duplicados/mapeo_dedup_copy.bam \
                              -O ./6.Limpieza_duplicados/mapeo_dedup.bam \
                              -RGID {RGID.get()} \
                              -RGLB {RGLB.get()} \
                              -RGPL {RGPL.get()} \
                              -RGSM {RGSM.get()} \
                              -RGPU {RGPU.get()}")

##### 7. Llamada de variantes #####
    @reactive.effect
    def comando7_a_actualizacion():
        comando7_a_actual.set("mkdir 7.Llamada_variantes")
    
    @reactive.effect
    def comando7_b_actualizacion():
        comando7_b_actual.set(f"mv {nombre_archivo3_completo.get()} ./7.Llamada_variantes/{nombre_archivo3_completo.get()}")

    @reactive.effect
    def comando7_c_actualizacion():
        comando7_c_actual.set(f"samtools faidx ./7.Llamada_variantes/{nombre_archivo3_completo.get()}")
    
    @reactive.effect
    def comando7_d_actualizacion():
        comando7_d_actual.set("samtools index ./6.Limpieza_duplicados/mapeo_dedup.bam")

    @reactive.effect
    def comando7_e_actualizacion():
        comando7_e_actual.set(f"freebayes {ploidy.get()} {ploidy_num.get()} \
                              {min_alternate_fraction.get()} {min_alternate_fraction_num.get()} \
                              {min_alternate_count.get()} {min_alternate_count_num.get()} \
                              {min_mapping_quality.get()} {min_mapping_quality_num.get()} \
                              {opcion_adicional_7e.get()} \
                              -f ./7.Llamada_variantes/{nombre_archivo3_completo.get()} \
                              ./6.Limpieza_duplicados/mapeo_dedup.bam > ./7.Llamada_variantes/variantes.vcf")

    @reactive.effect
    def comando7_f_actualizacion():
        comando7_f_actual.set("rtg vcfstats ./7.Llamada_variantes/variantes.vcf > ./7.Llamada_variantes/informe_variantes.txt")

##### 8. Filtrado de variantes #####
    @reactive.effect
    def comando8_a_actualizacion():
        comando8_a_actual.set("mkdir 8.Filtrado_variantes")
    
    @reactive.effect
    def comando8_b0_actualizacion():
        comando8_b0_actual.set("cp ./7.Llamada_variantes/variantes.vcf ./8.Filtrado_variantes/variantes.vcf")

    @reactive.effect
    def comando8_b_actualizacion():
        comando8_b_actual.set("cp ./7.Llamada_variantes/variantes.vcf ./7.Llamada_variantes/variantes_copy.vcf")

    @reactive.effect
    def comando8_actualizacion():
        comando8_actual.set(f"vcftools --vcf ./7.Llamada_variantes/variantes_copy.vcf \
                            --recode --recode-INFO-all \
                            --out ./8.Filtrado_variantes/variantes.vcf \
                            {minQ.get()} {minQ_num.get()} \
                            {minDP.get()} {minDP_num.get()} \
                            {maxDP.get()} {maxDP_num.get()} \
                            {remove_indels.get()} \
                            {keep_only_indels.get()} \
                            {opcion_adicional_8.get()}")

    @reactive.effect
    def comando8_c_actualizacion():
        comando8_c_actual.set("mv ./8.Filtrado_variantes/variantes.vcf.recode.vcf ./8.Filtrado_variantes/variantes.vcf")
    
    @reactive.effect
    def comando8_d_actualizacion():
        comando8_d_actual.set("rtg vcfstats ./8.Filtrado_variantes/variantes.vcf > ./8.Filtrado_variantes/informe_variantes_filtradas.txt")


##### 9. Efecto de las variantes #####

    @reactive.effect
    def comando9_a_actualizacion():
        comando9_a_actual.set("mkdir 9.Efecto_variantes")

    @reactive.effect
    def comando9_actualizacion():
        comando9_actual.set(f"vep -i ./8.Filtrado_variantes/variantes.vcf \
                            -o ./9.Efecto_variantes/efecto_variantes.tsv \
                            --database --species homo_sapiens --force_overwrite --tab \
                            {assembly.get()} {assembly_valor.get()} \
                            {clin_sig_allele.get()} {clin_sig_allele_valor.get()} \
                            {sift.get()} {sift_valor.get()} \
                            {polyphen.get()} {polyphen_valor.get()} \
                            {gene_phenotype.get()} \
                            {variant_class.get()} \
                            {symbol.get()} \
                            {protein.get()} \
                            {hgvs.get()} \
                            {spdi.get()} \
                            {check_existing.get()} \
                            {uniprot.get()} \
                            {af.get()} \
                            {opcion_adicional_9.get()} \
                            {fields.get()} {fields_valor.get()}")

########################### APARTADOS DEL PROGRAMA ############################

#################### 0. Inicio ####################

# 0. Texto de introducción a la aplicación
    @render.text
    def texto_introduccion():
        return ui.HTML('GenAgans es una aplicación que le permitirá realizar el flujo de trabajo de análisis de variantes genéticas \
                       en humanos a partir de lecturas pareadas de forma interactiva, intuitiva y personalizada. <br>\
                       <br>\
                       Intrucciones de uso: <br>\
                       - Cargue los archivos de lecturas (formato FASTQ.gz) y el genoma de referencia (formato FASTA). <br>\
                       - Los botones avance se irán activando conforme vaya completando los diferentes pasos. Sígalos. <br>\
                       - Visualice los resultados obtenidos para tomar decisiones sobre las opciones disponibles. <br>\
                       - En cualquier momento puede consultar el apartado de resumen y/o descargar los archivos generados.')
    
# 0. Carga del archivo 1 (1o lecturas)
    @render.text
    def archivo1_nombre():
        if input.archivo1() is None:
            return "Nada cargado"
        else:
            ruta_archivo1 = input.archivo1()[0]["datapath"]
            nombre_archivo1 = input.archivo1()[0]["name"]
            reposicion_archivo1 = f"mv {ruta_archivo1} {ruta_archivos}/{nombre_archivo1}"
            subprocess.run(reposicion_archivo1, shell=True)
            return f"{nombre_archivo1}"

# 0. Carga del archivo 2 (2o lecturas)
    @render.text
    def  archivo2_nombre():
        if input.archivo2() is None:
            return "Nada cargado"
        else:
            ruta_archivo2 = input.archivo2()[0]["datapath"]
            nombre_archivo2 = input.archivo2()[0]["name"]
            reposicion_archivo2 = f"mv {ruta_archivo2} {ruta_archivos}/{nombre_archivo2}"
            subprocess.run(reposicion_archivo2, shell=True)
            return f"{nombre_archivo2}"

# 0. Carga del archivo 3 (genoma referencia)
    @render.text
    def  archivo3_nombre():
        if input.archivo3() is None:
            return "Nada cargado"
        else:
            ruta_archivo3 = input.archivo3()[0]["datapath"]
            nombre_archivo3 = input.archivo3()[0]["name"]
            reposicion_archivo3 = f"mv {ruta_archivo3} {ruta_archivos}/{nombre_archivo3}"
            subprocess.run(reposicion_archivo3, shell=True)
            return f"{nombre_archivo3}"

# 0. Activación de botones para EMPEZAR e inicio de calidad / Definición de los nombres de los archivos para futuras referencias
    @reactive.effect
    def botones_inicio_procesos01():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            ui.update_action_button("boton_empezar", disabled=False)
            ui.update_action_button("boton_analisis_calidad", disabled=False)
            extensiones = [".fastq.gz",".fq.gz"]
            nombre_archivo1 = input.archivo1()[0]["name"]
            nombre_archivo2 = input.archivo2()[0]["name"]
            nombre_archivo3 = input.archivo3()[0]["name"]
            archivo1_sin_extensiones = nombre_archivo1
            archivo2_sin_extensiones = nombre_archivo2
            for i in extensiones:
                archivo1_sin_extensiones = archivo1_sin_extensiones.replace(i,'')
                archivo2_sin_extensiones = archivo2_sin_extensiones.replace(i,'')
            nombre_archivo1_completo.set(nombre_archivo1)
            nombre_archivo2_completo.set(nombre_archivo2)
            nombre_archivo3_completo.set(nombre_archivo3)
            nombre_archivo1_sin_extensiones.set(archivo1_sin_extensiones)
            nombre_archivo2_sin_extensiones.set(archivo2_sin_extensiones)
        else:
            ui.update_action_button("boton_empezar", disabled=True)

# 0. Paso del apartado 0 (inicio) al apartado 1-Control de calidad
    @reactive.effect
    @reactive.event(input.boton_empezar)
    def inicio_a_1():
        ui.update_navs("panel", selected="1. Control de calidad de las lecturas")
        

#################### 1. Control de calidad ####################

# 1. Texto de la caja para el comando 1 en función de si se cargaron los archivos o no
    @render.text
    def comando1():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando1_actual.get()
        else:
            return "Cargue los archivos, por favor."

# 1. Creación de la carpeta 1 / Ejecución del comando 1 / Lectura de los htmls generados / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_analisis_calidad)
    def analisis_calidad_lecturas_inicio():
        comando1a_ejecutado.set(comando1_a_actual.get())
        comando1_ejecutado.set(comando1_actual.get())
        with ui.Progress(min=1, max=18) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta1 = comando1_a_actual.get()
            subprocess.run(crear_carpeta1, shell=True)
            barra.set(8)
            correr_analisis_calidad = comando1_actual.get()
            subprocess.run(correr_analisis_calidad, shell=True)
            barra.set(13)
            analisis_calidad_completado.set(True)
            with open(f"./1.Analisis_calidad/{nombre_archivo1_sin_extensiones.get()}_fastqc.html") as archivo:
                raw_html = archivo.readlines()
                cadena = """""".join(raw_html)
            resultado_html1_calidad.set(cadena)
            barra.set(15)
            with open(f"./1.Analisis_calidad/{nombre_archivo2_sin_extensiones.get()}_fastqc.html") as archivo:
                raw_html = archivo.readlines()
                cadena = """""".join(raw_html)
            resultado_html2_calidad.set(cadena)
            barra.set(18)


# 1. Renderizado del html del archivo 1 por pantalla
    @render.ui
    def html1_calidad():
        return ui.HTML(resultado_html1_calidad.get())
    
# 1. Renderizado del html del archivo 2 por pantalla
    @render.ui
    def html2_calidad():
        return ui.HTML(resultado_html2_calidad.get())

# 1. Compresión y descarga de los archivos generados con el comando 1
    @render.download
    def descarga_resultados1():
        with zipfile.ZipFile("Resultados_control_calidad.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./1.Analisis_calidad/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_control_calidad.zip"

# 1. Activación del botón siguiente del apartado 1 si la ejecución del comando 1 finalizó
    @reactive.effect
    def siguiente1():
        if analisis_calidad_completado.get() is True:
            ui.update_action_button("boton_siguiente1", disabled=False)

# 1. Paso del apartado 1 al apartado 2
    @reactive.effect
    @reactive.event(input.boton_siguiente1)
    def de1_a_2():
        ui.update_navs("panel", selected="2. Limpieza de las lecturas")


#################### 2. Limpieza de las lecturas ####################

# 2. Definición de todas las cajas de opciones para el comando 2
    @reactive.effect
    def Q_media_comando():
        if input.check_Q_media() is True:
            cut_mean_quality.set("--cut_mean_quality")
            cut_mean_quality_num.set(input.Q_media())
        else:
            cut_mean_quality.set("")
            cut_mean_quality_num.set("")

    @reactive.effect
    def Q_inicio_comando():
        if input.check_Q_inicio() is True:
            cut_front.set("--cut_front")
            cut_front_num.set(input.Q_inicio())
        else:
            cut_front.set("")
            cut_front_num.set("")

    @reactive.effect
    def Q_final_comando():
        if input.check_Q_final() is True:
            cut_tail.set("--cut_tail")
            cut_tail_num.set(input.Q_final())
        else:
            cut_tail.set("")
            cut_tail_num.set("")

    @reactive.effect
    def longitud_comando():
        if input.check_longitud() is True:
            longitud_l.set("-l")
            longitud_num.set(input.longitud())
        else:
            longitud_l.set("")
            longitud_num.set("")

    @reactive.effect
    def adaptadores_comando():
        if input.check_adaptadores() is True:
            detect_adapter_for_pe.set("--detect_adapter_for_pe")
        else:
            detect_adapter_for_pe.set("")
    
    @reactive.effect
    def polyG_comando():
        if input.check_polyG() is True:
            trim_poly_g.set("--trim_poly_g")
        else:
            trim_poly_g.set("")
    
    @reactive.effect
    def polyX_comando():
        if input.check_polyX() is True:
            trim_poly_x.set("--trim_poly_x")
        else:
            trim_poly_x.set("")

    @reactive.effect
    def opcion_adicional2():
        if input.opcion_adicional2() is not None:
            return opcion_adicional_2.set(input.opcion_adicional2())

# 2. Texto de aviso sobre que este paso es opcional
    @render.text
    def Opcional_limpieza():
        return ui.HTML('Si realmente considera que sus archivos de lecturas no requieren ningún tipo de limpieza \
                       puede proceder directamente al siguiente apartado.')

# 2. Activación del botón de siguiente de arriba del apartado 2 si la ejecución del comando 1 ha finalizado
    @reactive.effect
    def siguiente2a():
        if analisis_calidad_completado.get() is True and limpieza_lecturas_completado.get() is False:
            ui.update_action_button("boton_siguiente2a", disabled=False)
        else:
            ui.update_action_button("boton_siguiente2a", disabled=True)

# 2. Crear carpeta 2 / Copia de los archivos del apartado 1 / Paso del apartado 2 al 3 botón arriba
    @reactive.effect
    @reactive.event(input.boton_siguiente2a)
    def de2_a_3a():
        comando2a_ejecutado.set(comando2_a_actual.get())
        comando2b1_ejecutado.set(comando2_b1_actual.get())
        comando2b2_ejecutado.set(comando2_b2_actual.get())
        comando2_ejecutado.set("")
        with ui.Progress(min=1, max=18) as barra:
            barra.set(message="Organizando arhivos...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta2 = comando2_a_actual.get()
            subprocess.run(crear_carpeta2, shell=True)
            barra.set(8)
            copiar_fastq1 = comando2_b1_actual.get()
            subprocess.run(copiar_fastq1, shell=True)
            barra.set(13)
            copiar_fastq2 = comando2_b2_actual.get()
            subprocess.run(copiar_fastq2, shell=True)
            barra.set(18)
            salto_apartado2.set(True)
            ui.update_navs("panel", selected="3. Indexado del genoma de referencia")

# 2. Texto de la caja para el comando 2 en función de si se han cargado los archivos
    @render.text
    def comando2():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando2_actual.get()
        else:
           return "Cargue los archivos, por favor."
    
# 2. Activación del botón de inicio del comando 2 si la ejecución del comando 1 terminó
    @reactive.effect
    def boton_inicio_proceso2():
        if analisis_calidad_completado.get() is True:
            ui.update_action_button("boton_limpieza_lecturas", disabled=False)

# 2. Creación de la carpeta 2 / Ejecución del comando 2 / Lectura de los htmls generados / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_limpieza_lecturas)
    def limpieza_lecturas_inicio():
        comando2a_ejecutado.set(comando2_a_actual.get())
        comando2_ejecutado.set(comando2_actual.get())
        comando2b1_ejecutado.set("")
        comando2b2_ejecutado.set("")
        with ui.Progress(min=1, max=15) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta2 = comando2_a_actual.get()
            subprocess.run(crear_carpeta2, shell=True)
            barra.set(8)
            correr_limpieza_lecturas = comando2_actual.get()
            subprocess.run(correr_limpieza_lecturas, shell=True)
            barra.set(13)
            limpieza_lecturas_completado.set(True)
            with open(f"./2.Lecturas_limpias/{nombre_archivo1_sin_extensiones.get()}_{nombre_archivo2_sin_extensiones.get()}_fastp.html") as archivo:
                raw_html = archivo.readlines()
                cadena = """""".join(raw_html)
            resultado_html_limpieza_lecturas.set(cadena)
            barra.set(15)
    
# 2. Limpieza del html generado porque contiene un head con javascript problemático
    def limpiar_html(html_sucio, tag_inicio_html, tag_final_html):
        if tag_inicio_html in html_sucio:
            indice1 = html_sucio.index(tag_inicio_html)
            indice2 = html_sucio.index(tag_final_html)
            contenido = ''
            for indice in range(indice1 + len(tag_inicio_html), indice2):
                contenido = contenido + html_sucio[indice]
            html_limpio = html_sucio.replace(tag_inicio_html + contenido + tag_final_html, "")
        else:
            html_limpio = html_sucio
        return html_limpio

# 2. Renderizado del html limpio
    @render.ui
    def html_limpieza_lecturas():
        html2_limpio = limpiar_html(resultado_html_limpieza_lecturas.get(), "<head>", "</head>")
        return ui.HTML(html2_limpio)

# 2. Compresión y descarga de los archivos generados con el comando 2
    @render.download
    def descarga_resultados2():
        with zipfile.ZipFile("Resultados_limpieza_lecturas.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./2.Lecturas_limpias/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_limpieza_lecturas.zip"

# 2. Activación del botón siguiente del apartado 2 si la ejecución del comando 2 ha finalizado
    @reactive.effect
    def siguiente2():
        if limpieza_lecturas_completado.get() is True:
            ui.update_action_button("boton_siguiente2", disabled=False)

# 2. Paso del apartado 2 al 3
    @reactive.effect
    @reactive.event(input.boton_siguiente2)
    def de2_a_3():
        ui.update_navs("panel", selected="3. Indexado del genoma de referencia")


#################### 3. Indexado ####################

# 3. Texto de la caja para el comando 3 en función de si se han cargado los archivos
    @render.text
    def comando3():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando3_actual.get()
        else:
           return "Cargue los archivos, por favor."

# 3. Activación del botón de inicio del comando 3 si la ejecución del comando 2 terminó
    @reactive.effect
    def boton_inicio_proceso3():
        if limpieza_lecturas_completado.get() is True or salto_apartado2.get() is True:
            ui.update_action_button("boton_indexado", disabled=False)

# 3. Creación de la carpeta 3 / Ejecución del comando 3 / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_indexado)
    def indexado_inicio():
        comando3a_ejecutado.set(comando3_a_actual.get())
        comando3b_ejecutado.set(comando3_b_actual.get())
        comando3_ejecutado.set(comando3_actual.get())
        with ui.Progress(min=1, max=18) as barra:
            barra.set(message="Procesando...", detail="Este proceso puede ser especialmente pesado. Espere, por favor.")
            barra.set(3)
            crear_carpeta3 = comando3_a_actual.get()
            subprocess.run(crear_carpeta3, shell=True)
            barra.set(8)
            copiar_genoma_ref = comando3_b_actual.get()
            subprocess.run(copiar_genoma_ref, shell=True)
            barra.set(13)
            correr_indexado = comando3_actual.get()
            subprocess.run(correr_indexado, shell=True)
            barra.set(18)
            indexado_completado.set(True)

# 3. Compresión y descarga de los archivos generados con el comando 3
    @render.download
    def descarga_resultados3():
        with zipfile.ZipFile("Resultados_indexado.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./3.Genoma_referencia_indexado/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_indexado.zip"

# 3. Activación del botón siguiente del apartado 3 si la ejecución del comando 3 ha finalizado
    @reactive.effect
    def siguiente3():
        if indexado_completado.get() is True:
            ui.update_action_button("boton_siguiente3", disabled=False)

# 3. Paso del apartado 3 al 4
    @reactive.effect
    @reactive.event(input.boton_siguiente3)
    def de3_a_4():
        ui.update_navs("panel", selected="4. Mapeo")


#################### 4. Mapeo ####################

# 4. Texto de la caja para el comando 4 en función de si se han cargado los archivos
    @render.text
    def comando4():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando4_actual.get()
        else:
           return "Cargue los archivos, por favor."

# 4. Activación del botón de inicio del comando 4 si la ejecución del comando 3 terminó
    @reactive.effect
    def boton_inicio_proceso4():
        if indexado_completado.get() is True:
            ui.update_action_button("boton_mapeo", disabled=False)

# 4. Creación de la carpeta 4 / Ejecución del comando 4 / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_mapeo)
    def mapeo_inicio():
        comando4a_ejecutado.set(comando4_a_actual.get())
        comando4_ejecutado.set(comando4_actual.get())
        with ui.Progress(min=1, max=18) as barra:
            barra.set(message="Procesando...", detail="Este proceso puede ser especialmente pesado. Espere, por favor.")
            barra.set(3)
            crear_carpeta4 = comando4_a_actual.get()
            subprocess.run(crear_carpeta4, shell=True)
            barra.set(8)
            correr_mapeo = comando4_actual.get()
            subprocess.run(correr_mapeo, shell=True)
            barra.set(18)
            mapeo_completado.set(True)

# 4. Compresión y descarga del archivo generado con el comando 4
    @render.download
    def descarga_resultados4():
        with zipfile.ZipFile("Resultados_mapeo.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./4.Mapeo/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_mapeo.zip"

# 4. Activación del botón siguiente 4 si la ejecución del comando 4 ha finalizado
    @reactive.effect
    def siguiente4():
        if mapeo_completado.get() is True:
            ui.update_action_button("boton_siguiente4", disabled=False)

# 4. Paso del apartado 4 al 5
    @reactive.effect
    @reactive.event(input.boton_siguiente4)
    def de4_a_5():
        ui.update_navs("panel", selected="5. Análisis del mapeo")


#################### 5. Análisis del mapeo ####################

# 5. Texto de la caja para el comando 5b en función de si se han cargado los archivos
    @render.text
    def comando5b():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando5_b_actual.get()
        else:
           return "Cargue los archivos, por favor."
        
# 5. Texto de la caja para el comando 5c en función de si se han cargado los archivos
    @render.text
    def comando5c():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando5_c_actual.get()
        else:
           return "Cargue los archivos, por favor."

# 5. Texto de la caja para el comando 5 en función de si se han cargado los archivos
    @render.text
    def comando5():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando5_actual.get()
        else:
           return "Cargue los archivos, por favor."

# 5. Texto de la caja para el comando 5d en función de si se han cargado los archivos
    @render.text
    def comando5d():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando5_d_actual.get()
        else:
           return "Cargue los archivos, por favor."

# 5. Activación del botón de inicio del comando 5 si la ejecución del comando 4 terminó
    @reactive.effect
    def boton_inicio_proceso5():
        if mapeo_completado.get() is True:
            ui.update_action_button("boton_analisis_mapeo", disabled=False)

# 5. Función para codificar una imagen a base 64 y decodificarla en utf-8
    def img_a_base64(ruta_img):
        with open(ruta_img, "rb") as imagen:
            imagen_codificada = base64.b64encode(imagen.read())
        return imagen_codificada.decode("utf-8")

# 5. Función para sustituir en el html las rutas de las imágenes a las imágenes en base 64
    def cambio_imgs_a_base64(html_sucio, img_originales):
        html_limpio = html_sucio
        for img in img_originales:
            ruta_img = "./5.Analisis_mapeo/" + img
            img_base64 = img_a_base64(ruta_img)
            html_limpio = html_limpio.replace(img, "data:image/png;base64," + img_base64)
        return html_limpio

# 5. Creación de la carpeta 5 / Ejecución del comando 5 / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_analisis_mapeo)
    def analisis_mapeo_inicio():
        comando5a_ejecutado.set(comando5_a_actual.get())
        comando5b_ejecutado.set(comando5_b_actual.get())
        comando5c_ejecutado.set(comando5_c_actual.get())
        comando5_ejecutado.set(comando5_actual.get())
        comando5d_ejecutado.set(comando5_d_actual.get())
        with ui.Progress(min=1, max=38) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta5 = comando5_a_actual.get()
            subprocess.run(crear_carpeta5, shell=True)
            barra.set(8)
            sam_a_bam = comando5_b_actual.get()
            subprocess.run(sam_a_bam, shell=True)
            barra.set(13)
            ordenar_bam = comando5_c_actual.get()
            subprocess.run(ordenar_bam, shell=True)
            barra.set(18)
            correr_analisis_mapeo = comando5_actual.get()
            subprocess.run(correr_analisis_mapeo, shell=True)
            barra.set(23)
            correr_html_analisis_mapeo = comando5_d_actual.get()
            subprocess.run(correr_html_analisis_mapeo, shell=True)
            barra.set(28)
            analisis_mapeo_completado.set(True)
            with open("./5.Analisis_mapeo/informe_mapeo.html") as archivo:
                raw_html = archivo.readlines()
                cadena = """""".join(raw_html)
            resultado_html_analisis_mapeo.set(cadena)
            barra.set(33)
            nombres_imagenes = ["informe_mapeo-acgt-cycles.png", "informe_mapeo-coverage.png", "informe_mapeo-gc-content.png", 
                            "informe_mapeo-gc-depth.png", "informe_mapeo-indel-cycles.png", "informe_mapeo-indel-dist.png", 
                            "informe_mapeo-insert-size.png", "informe_mapeo-quals.png", "informe_mapeo-quals2.png", 
                            "informe_mapeo-quals3.png", "informe_mapeo-quals-hm.png", "informe_mapeo-read_length.png"]
            html_imgs_a_base64 = cambio_imgs_a_base64(resultado_html_analisis_mapeo.get(), nombres_imagenes)
            resultado_html_analisis_mapeo.set("<div class='html_content'>" + html_imgs_a_base64 + "</div>")
            barra.set(38)

# 5. Renderizado del html del comando 5 por pantalla
    @render.ui
    def html_analisis_mapeo():
        return ui.HTML(resultado_html_analisis_mapeo.get())

# 5. Compresión y descarga del archivo generado con el comando 5
    @render.download
    def descarga_resultados5():
        with zipfile.ZipFile("Resultados_analisis_mapeo.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./5.Analisis_mapeo/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_analisis_mapeo.zip"

# 5. Activación del botón siguiente 5 si la ejecución del comando 5 ha finalizado
    @reactive.effect
    def siguiente5():
        if analisis_mapeo_completado.get() is True:
            ui.update_action_button("boton_siguiente5", disabled=False)

# 5. Paso del apartado 5 al 6
    @reactive.effect
    @reactive.event(input.boton_siguiente5)
    def de5_a_6():
        ui.update_navs("panel", selected="6. Limpieza de duplicados")


#################### 6. Limpieza de duplicados ####################

# 6. Definición de todas las cajas de opciones para el comando 6d controladas por el check de Read Groups
    @reactive.effect
    def RGID_comando():
        if input.check_ReadGroups() is not None:
            return RGID.set(input.rgid())
    
    @reactive.effect
    def RGLB_comando():
        if input.check_ReadGroups() is not None:
            return RGLB.set(input.rglibreria())
    
    @reactive.effect
    def RGPL_comando():
        if input.check_ReadGroups() is not None:
            return RGPL.set(input.rgplataforma())
    
    @reactive.effect
    def RGPU_comando():
        if input.check_ReadGroups() is not None:
            return RGPU.set(input.rgcarrera())
    
    @reactive.effect
    def RGSM_comando():
        if input.check_ReadGroups() is not None:
            return RGSM.set(input.rgmuestra())
    
# 6. Texto de la caja para el comando 6b en función de si se cargaron los archivos
    @render.text
    def comando6b():
        if input.archivo1() is None and input.archivo2() is None and input.archivo3() is None:
            return "Cargue los archivos, por favor."
        else:
            return comando6_b_actual.get()

# 6. Activación del botón de inicio del comando 6b si la ejecución del comando 5 terminó
    @reactive.effect
    def boton_inicio_proceso6b():
        if analisis_mapeo_completado.get() is True:
            ui.update_action_button("boton_marcar_duplicados", disabled=False)

# 6. Renderizado del txt del comando 6b por pantalla
    @render.ui
    def txt_Duplicados():
        return ui.HTML(resultado_txt_Duplicados.get())

# 6. Creación de la carpeta 6 / Ejecución del comando 6b: marcaje de duplicados / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_marcar_duplicados)
    def marcaje_duplicados_inicio():
        comando6a_ejecutado.set(comando6_a_actual.get())
        comando6b_ejecutado.set(comando6_b_actual.get())
        with ui.Progress(min=1, max=15) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta6 = comando6_a_actual.get()
            subprocess.run(crear_carpeta6, shell=True)
            barra.set(8)
            correr_marcaje_duplicados = comando6_b_actual.get()
            subprocess.run(correr_marcaje_duplicados, shell=True)
            comando6_b_completado.set(True)
            barra.set(13)
            cadena = ""
            with open("./6.Limpieza_duplicados/MarkDuplicatesMetrics.txt") as archivo:
                raw_txt = archivo.readlines()
                for line in raw_txt:
                    cadena += line + "<br>"
            resultado_txt_Duplicados.set(cadena)
            barra.set(15)

# 6. Texto de aviso sobre los Read Groups
    @render.text
    def Disclaimer():
        return ui.HTML('Los Read Groups (RG) son metadatos identificativos para las lecturas secuenciadas \
                    necesarios para realizar la llamada de variantes. <br> \
                    A continuación se realiza una comprobación de los RG presentes en el archivo de mapeo generado. <br> \
                    Los campos esperados son: "ID", "LB", "PL", "PU" y "SM". En función de lo observado en el informe deberá tomar \
                    una decisión: <br> \
                    - Si el informe aparece vacío, será necesaria su adición. Para ello emplee el último comando de este apartado. <br> \
                    - Si el informe muestra RG pero no para todos los campos, también será necesaria su adición. \
                    Para ello emplee el último comando de este apartado (tenga en cuenta que se reemplazarán los valores actuales). <br> \
                    - Si el informe muestra RG para todos los campos, no será necesaria su adición. Puede ignorar el último comando \
                    de este apartado y seguir adelante.')

# 6. Texto de la caja para el comando 6c en función de si la ejecución del comando 6b finalizó y/o se cargaron los archivos
    @render.text
    def comando6c():
        if input.archivo1() is None and input.archivo2() is None and input.archivo3() is None:
            return "Cargue los archivos, por favor."
        else:
            if comando6_b_completado.get() is False:
                return "Marque los duplicados, por favor."
            else:
                return comando6_c_actual.get()

# 6. Activación del botón de inicio del comando 6c si la ejecución del comando 6b terminó
    @reactive.effect
    def boton_inicio_proceso6c():
        if comando6_b_completado.get() is True:
            ui.update_action_button("boton_comprobar_ReadGroups", disabled=False)

# 6. Ejecución del comando 6c: comprobación de los Read Groups / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_comprobar_ReadGroups)
    def comprobacion_ReadGroups_inicio():
        comando6c_ejecutado.set(comando6_c_actual.get())
        with ui.Progress(min=1, max=13) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            comprobar_RG = comando6_c_actual.get()
            subprocess.run(comprobar_RG, shell=True)
            barra.set(8)
            with open("./6.Limpieza_duplicados/ReadGroups.txt") as archivo:
                raw_txt = archivo.readlines()
                cadena = """""".join(raw_txt)
            resultado_txt_ReadGroups.set(cadena)
            comando6_c_completado.set(True)
            barra.set(13)

# 6. Renderizado del txt del comando 6c por pantalla
    @render.ui
    def txt_ReadGroups():
        return ui.HTML(resultado_txt_ReadGroups.get())
    
# 6. Texto de la caja para el comando 6d en función de si se han cargado los archivos y/o el 6c finalizó y/o se activó el check Read Groups
    @render.text
    def comando6d():
        if input.archivo1() is None and input.archivo2() is None and input.archivo3() is None:
            return "Cargue los archivos, por favor."
        else:
            if comando6_c_completado.get() is False:
                return "Compruebe los Read Groups, por favor."
            else:
                if input.check_ReadGroups() is False:
                    return "Esperando decisión..."
                else:
                    return comando6_d_actual.get()

# 6. Activación del botón de inicio del comando 6d si la ejecución del comando 6b terminó y se activó el check Read Groups
    @reactive.effect
    def boton_inicio_proceso6d():
        if comando6_c_completado.get() is True and input.check_ReadGroups() is True:
            ui.update_action_button("boton_añadir_ReadGroups", disabled=False)
        else:
            ui.update_action_button("boton_añadir_ReadGroups", disabled=True)

# 6. Ejecución del comando 6d: marcaje de duplicados / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_añadir_ReadGroups)
    def adicion_ReadGroups_inicio():
        comando6d0_ejecutado.set(comando6_d0_actual.get())
        comando6d_ejecutado.set(comando6_d_actual.get())
        with ui.Progress(min=1, max=13) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            cambio_nombre_bam = comando6_d0_actual.get()
            subprocess.run(cambio_nombre_bam, shell=True)
            barra.set(8)
            adicion_RG = comando6_d_actual.get()
            subprocess.run(adicion_RG, shell=True)
            barra.set(13)

# 6. Compresión y descarga de los archivos generados con los comandos 6
    @render.download
    def descarga_resultados6():
        with zipfile.ZipFile("Resultados_limpieza_duplicados.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./6.Limpieza_duplicados/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_limpieza_duplicados.zip"

# 6. Activación del botón siguiente del apartado 6 si la ejecución del comando 6c (comprobación de Read Groups) ha finalizado
    @reactive.effect
    def siguiente6():
        if comando6_c_completado.get() is True:
            ui.update_action_button("boton_siguiente6", disabled=False)

# 6. Paso del apartado 6 al 7
    @reactive.effect
    @reactive.event(input.boton_siguiente6)
    def de6_a_7():
        ui.update_navs("panel", selected="7. Llamada de variantes")


#################### 7. Llamada de variantes ####################

# 7. Definición de todas las cajas de opciones para el comando 7e controladas por por sus propios checks
    @reactive.effect
    def ploidia_comando():
        if input.check_ploidia() is True:
            ploidy.set("--ploidy")
            ploidy_num.set(input.ploidia())
        else:
            ploidy.set("")
            ploidy_num.set("")
    
    @reactive.effect
    def min_frecuencia_comando():
        if input.check_min_frecuencia() is True:
            min_alternate_fraction.set("--min-alternate-fraction")
            min_alternate_fraction_num.set(input.min_frecuencia())
        else:
            min_alternate_fraction.set("")
            min_alternate_fraction_num.set("")

    @reactive.effect
    def min_lecturas_comando():
        if input.check_min_lecturas() is True:
            min_alternate_count.set("--min-alternate-count")
            min_alternate_count_num.set(input.min_lecturas())
        else:
            min_alternate_count.set("")
            min_alternate_count_num.set("")

    @reactive.effect
    def min_calidad_mapeo_comando():
        if input.check_min_calidad_mapeo() is True:
            min_mapping_quality.set("--min-mapping-quality")
            min_mapping_quality_num.set(input.min_calidad_mapeo())
        else:
            min_mapping_quality.set("")
            min_mapping_quality_num.set("")
    
    @reactive.effect
    def opcion_adicional7e_comando():
        if input.opcion_adicional7e() is not None:
            return opcion_adicional_7e.set(input.opcion_adicional7e())
    
# 7. Texto de la caja para el comando 7c en función de si se cargaron los archivos
    @render.text
    def comando7c():
        if input.archivo1() is None and input.archivo2() is None and input.archivo3() is None:
            return "Cargue los archivos, por favor."
        else:
            return comando7_c_actual.get()

# 7. Texto de la caja para el comando 7d en función de si se cargaron los archivos
    @render.text
    def comando7d():
        if input.archivo1() is None and input.archivo2() is None and input.archivo3() is None:
            return "Cargue los archivos, por favor."
        else:
            return comando7_d_actual.get()

# 7. Texto de la caja para el comando 7e en función de si se cargaron los archivos
    @render.text
    def comando7e():
        if input.archivo1() is None and input.archivo2() is None and input.archivo3() is None:
            return "Cargue los archivos, por favor."
        else:
            return comando7_e_actual.get()

# 7. Texto de la caja para el comando 7f en función de si se cargaron los archivos
    @render.text
    def comando7f():
        if input.archivo1() is None and input.archivo2() is None and input.archivo3() is None:
            return "Cargue los archivos, por favor."
        else:
            return comando7_f_actual.get()

# 7. Activación del botón de inicio de los comandos 7 si la ejecución de los comandos 6 terminó
    @reactive.effect
    def boton_inicio_proceso7():
        if comando6_c_completado.get() is True:
            ui.update_action_button("boton_llamada_variantes", disabled=False)

# 7. Creación de la carpeta 7 / Ejecución del comando 7b, 7c, 7d, 7e y 7f / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_llamada_variantes)
    def llamada_de_variantes_inicio():
        comando7a_ejecutado.set(comando7_a_actual.get())
        comando7b_ejecutado.set(comando7_b_actual.get())
        comando7c_ejecutado.set(comando7_c_actual.get())
        comando7d_ejecutado.set(comando7_d_actual.get())
        comando7e_ejecutado.set(comando7_e_actual.get())
        comando7f_ejecutado.set(comando7_f_actual.get())
        with ui.Progress(min=1, max=38) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta7 = comando7_a_actual.get()
            subprocess.run(crear_carpeta7, shell=True)
            barra.set(8)
            mover_genoma_referencia = comando7_b_actual.get()
            subprocess.run(mover_genoma_referencia, shell=True)
            barra.set(13)
            correr_indexado_genoma = comando7_c_actual.get()
            subprocess.run(correr_indexado_genoma, shell=True)
            barra.set(18)
            correr_indexado_mapeo = comando7_d_actual.get()
            subprocess.run(correr_indexado_mapeo, shell=True)
            barra.set(23)
            correr_llamada_variantes = comando7_e_actual.get()
            subprocess.run(correr_llamada_variantes, shell=True)
            barra.set(28)
            crear_html_variantes = comando7_f_actual.get()
            subprocess.run(crear_html_variantes, shell=True)
            barra.set(33)
            llamada_variantes_completado.set(True)
            cadena = ""
            with open("./7.Llamada_variantes/informe_variantes.txt") as archivo:
                raw_txt = archivo.readlines()
                for line in raw_txt:
                    cadena += line + "<br>"
            resultado_txt_llamada_variantes.set(cadena)
            barra.set(38)

# 7. Renderizado del html del comando 7f por pantalla
    @render.ui
    def txt_llamada_variantes():
        return ui.HTML(resultado_txt_llamada_variantes.get())

# 7. Compresión y descarga de los archivos generados con los comandos 7
    @render.download
    def descarga_resultados7():
        with zipfile.ZipFile("Resultados_llamada_variantes.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./7.Llamada_variantes/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_llamada_variantes.zip"

# 7. Activación del botón siguiente del apartado 7 si la ejecución del comando 7f ha finalizado
    @reactive.effect
    def siguiente7():
        if llamada_variantes_completado.get() is True:
            ui.update_action_button("boton_siguiente7", disabled=False)

# 7. Paso del apartado 7 al 8
    @reactive.effect
    @reactive.event(input.boton_siguiente7)
    def de7_a_8():
        ui.update_navs("panel", selected="8. Filtrado de variantes")


#################### 8. Filtrado de variantes ####################

# 8. Definición de todas las cajas de opciones para el comando 8
    @reactive.effect
    def minQ_comando():
        if input.check_calidad_variantes() is True:
            minQ.set("--minQ")
            minQ_num.set(input.calidad_variantes())
        else:
            minQ.set("")
            minQ_num.set("")

    @reactive.effect
    def minDP_comando():
        if input.check_profundidad_min() is True:
            minDP.set("--minDP")
            minDP_num.set(input.profundidad_min())
        else:
            minDP.set("")
            minDP_num.set("")

    @reactive.effect
    def maxDP_comando():
        if input.check_profundidad_max() is True:
            maxDP.set("--maxDP")
            maxDP_num.set(input.profundidad_max())
        else:
            maxDP.set("")
            maxDP_num.set("")

    @reactive.effect
    def remove_indels_comando():
        if input.check_eliminar_indels() is True:
            remove_indels.set("--remove-indels")
            ui.update_checkbox("check_mantener_indels", value=False)
        else:
            remove_indels.set("")
    
    @reactive.effect
    def keep_only_indels_comando():
        if input.check_mantener_indels() is True:
            keep_only_indels.set("--keep-only-indels")
            ui.update_checkbox("check_eliminar_indels", value=False)
        else:
            keep_only_indels.set("")

    @reactive.effect
    def opcion_adicional8_comando():
        if input.opcion_adicional8() is not None:
            return opcion_adicional_8.set(input.opcion_adicional8())

# 8. Texto de aviso sobre que este paso es opcional
    @render.text
    def Opcional():
        return ui.HTML('Si no desea filtrar su archivo de variantes puede proceder directamente al siguiente apartado.')

# 8. Texto de la caja para el comando 8 en función de si se han cargado los archivos
    @render.text
    def comando8():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando8_actual.get()
        else:
           return "Cargue los archivos, por favor."

# 8. Texto de la caja para el comando 8d en función de si se han cargado los archivos
    @render.text
    def comando8d():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando8_d_actual.get()
        else:
           return "Cargue los archivos, por favor."
    
# 8. Activación del botón de inicio del comando 8 si la ejecución del comando 7f terminó
    @reactive.effect
    def boton_inicio_proceso8():
        if llamada_variantes_completado.get() is True:
            ui.update_action_button("boton_filtrado_variantes", disabled=False)

# 8. Creación de la carpeta 8 / Ejecución del comando 8 / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_filtrado_variantes)
    def filtrado_variantes_inicio():
        comando8a_ejecutado.set(comando8_a_actual.get())
        comando8b_ejecutado.set(comando8_b_actual.get())
        comando8_ejecutado.set(comando8_actual.get())
        comando8c_ejecutado.set(comando8_c_actual.get())
        comando8d_ejecutado.set(comando8_d_actual.get())
        comando8b0_ejecutado.set("")
        with ui.Progress(min=1, max=23) as barra:
            barra.set(message="Procesando...", detail="Este proceso puede ser especialmente pesado. Espere, por favor.")
            barra.set(3)
            crear_carpeta8 = comando8_a_actual.get()
            subprocess.run(crear_carpeta8, shell=True)
            barra.set(8)
            crear_copia_vcf = comando8_b_actual.get()
            subprocess.run(crear_copia_vcf, shell=True)
            barra.set(13)
            correr_filtrado_variantes = comando8_actual.get()
            subprocess.run(correr_filtrado_variantes, shell=True)
            barra.set(15)
            renombrar_vcf = comando8_c_actual.get()
            subprocess.run(renombrar_vcf, shell=True)
            barra.set(18)
            crear_informe_filtrado = comando8_d_actual.get()
            subprocess.run(crear_informe_filtrado, shell=True)
            barra.set(23)
            filtrado_variantes_completado.set(True)
            cadena = ""
            with open("./8.Filtrado_variantes/informe_variantes_filtradas.txt") as archivo:
                raw_txt = archivo.readlines()
                for line in raw_txt:
                    cadena += line + "<br>"
            resultado_txt_filtrado_variantes.set(cadena)
            barra.set(28)

# 8. Renderizado del html del comando 8 por pantalla
    @render.ui
    def txt_filtrado_variantes():
        return ui.HTML(resultado_txt_filtrado_variantes.get())

# 8. Compresión y descarga de los archivos generados con los comandos 8
    @render.download
    def descarga_resultados8():
        with zipfile.ZipFile("Resultados_filtrado_variantes.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./8.Filtrado_variantes/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_filtrado_variantes.zip"

# 8. Activación del botón de siguiente de arriba del apartado 8 si la ejecución del comando 7f ha finalizado
    @reactive.effect
    def siguiente8a():
        if llamada_variantes_completado.get() is True and filtrado_variantes_completado.get() is False:
            ui.update_action_button("boton_siguiente8a", disabled=False)
        else:
            ui.update_action_button("boton_siguiente8a", disabled=True)

# 8. Crear carpeta 8 / Copia del vcf del apartado 7 / Paso del apartado 8 al 9 botón arriba
    @reactive.effect
    @reactive.event(input.boton_siguiente8a)
    def de8_a_9a():
        comando8a_ejecutado.set(comando8_a_actual.get())
        comando8b0_ejecutado.set(comando8_b0_actual.get())
        comando8b_ejecutado.set("")
        comando8_ejecutado.set("")
        comando8c_ejecutado.set("")
        comando8d_ejecutado.set("")
        with ui.Progress(min=1, max=13) as barra:
            barra.set(message="Organizando arhivos...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta8 = comando8_a_actual.get()
            subprocess.run(crear_carpeta8, shell=True)
            barra.set(8)
            copiar_vcf = comando8_b0_actual.get()
            subprocess.run(copiar_vcf, shell=True)
            barra.set(13)
            salto_apartado8.set(True)
            ui.update_navs("panel", selected="9. Efecto de las variantes")

# 8. Activación del botón de siguiente de abajo del apartado 8 si se ha realizado el filtrado de variantes
    @reactive.effect
    def siguiente8b():
        if filtrado_variantes_completado.get() is True:
            ui.update_action_button("boton_siguiente8b", disabled=False)

# 8. Paso del apartado 8 al 9 botón abajo
    @reactive.effect
    @reactive.event(input.boton_siguiente8b)
    def de8_a_9b():
        ui.update_navs("panel", selected="9. Efecto de las variantes")


#################### 9. Efecto de las variantes ####################

# 9. Definición de todas las cajas de opciones para el comando 9
    @reactive.effect
    def assembly_comando():
        if input.check_assembly() is True:
            assembly.set("--assembly")
            assembly_valor.set(input.seleccion_assembly())
        else:
            assembly.set("")
            assembly_valor.set("")
    
    @reactive.effect
    def clin_sig_allele_comando():
        if input.check_clin_sig_allele() is True:
            clin_sig_allele.set("--clin_sig_allele")
            clin_sig_allele_valor.set(input.seleccion_clin_sig())
        else:
            clin_sig_allele.set("")
            clin_sig_allele_valor.set("")

    @reactive.effect
    def sift_comando():
        if input.check_sift() is True:
            sift.set("--sift")
            sift_valor.set(input.seleccion_sift())
        else:
            sift.set("")
            sift_valor.set("")

    @reactive.effect
    def polyphen_comando():
        if input.check_polyphen() is True:
            polyphen.set("--polyphen")
            polyphen_valor.set(input.seleccion_polyphen())
        else:
            polyphen.set("")
            polyphen_valor.set("")

    @reactive.effect
    def gene_phenotype_comando():
        if input.check_gene_phenotype() is True:
            gene_phenotype.set("--gene_phenotype")
        else:
            gene_phenotype.set("")

    @reactive.effect
    def variant_class_comando():
        if input.check_variant_class() is True:
            variant_class.set("--variant_class")
        else:
            variant_class.set("")
    
    @reactive.effect
    def symbol_comando():
        if input.check_symbol() is True:
            symbol.set("--symbol")
        else:
            symbol.set("")

    @reactive.effect
    def protein_comando():
        if input.check_protein() is True:
            protein.set("--protein")
        else:
            protein.set("")
    
    @reactive.effect
    def hgvs_comando():
        if input.check_hgvs() is True:
            hgvs.set("--hgvs")
        else:
            hgvs.set("")
    
    @reactive.effect
    def spdi_comando():
        if input.check_spdi() is True:
            spdi.set("--spdi")
        else:
            spdi.set("")

    @reactive.effect
    def check_existing_comando():
        if input.check_check_existing() is True:
            check_existing.set("--check_existing")
        else:
            check_existing.set("")

    @reactive.effect
    def uniprot_comando():
        if input.check_uniprot() is True:
            uniprot.set("--uniprot")
        else:
            uniprot.set("")

    @reactive.effect
    def af_comando():
        if input.check_af() is True:
            af.set("--af")
        else:
            af.set("")

    @reactive.effect
    def fields_comando():
        if input.check_fields() is True:
            fields.set("--fields")
            fields_valor.set(f'"{",".join(input.campos_seleccionados())}"')
        else:
            fields.set("")
            fields_valor.set("")

    @reactive.effect
    def opcion_adicional9_comando():
        if input.opcion_adicional9() is not None:
            return opcion_adicional_9.set(input.opcion_adicional9())

# 9. Texto de la caja para el comando 9 en función de si se han cargado los archivos
    @render.text
    def comando9():
        if input.archivo1() is not None and input.archivo2() is not None and input.archivo3() is not None:
            return comando9_actual.get()
        else:
           return "Cargue los archivos, por favor."
    
# 9. Activación del botón de inicio del comando 9 si la ejecución del comando 7f terminó
    @reactive.effect
    def boton_inicio_proceso9():
        if filtrado_variantes_completado.get() is True or salto_apartado8.get() is True:
            ui.update_action_button("boton_VEP", disabled=False)

# 9. Procesado de la tabla VEP: abrir el archivo, seleccionar las líneas que no empiezan por ## (tabla), unirlas, convetirlas a dataframe,
#    convetir el dataframe en html y guardar el html en un archivo
    def procesar_tabla_VEP():
        with open("./9.Efecto_variantes/efecto_variantes.tsv", 'r') as archivotsv:
            lineas_no_cabecera = [linea for linea in archivotsv if not linea.startswith('##')]
        lineas_tabla = ''.join(lineas_no_cabecera)
        dataframe_tabla = pd.read_csv(StringIO(lineas_tabla), sep='\t')
        tabla_html = dataframe_tabla.to_html(index=False)
        with open("./9.Efecto_variantes/tabla_efecto_variantes.html", "w") as archivohtml:
            archivohtml.write(tabla_html)

# 9. Creación de la carpeta 9 / Ejecución del comando 9 / Barra de carga
    @reactive.effect
    @reactive.event(input.boton_VEP)
    def efecto_variantes_inicio():
        comando9a_ejecutado.set(comando9_a_actual.get())
        comando9_ejecutado.set(comando9_actual.get())
        with ui.Progress(min=1, max=28) as barra:
            barra.set(message="Procesando...", detail="Espere, por favor.")
            barra.set(3)
            crear_carpeta9 = comando9_a_actual.get()
            subprocess.run(crear_carpeta9, shell=True)
            barra.set(8)
            predecir_efecto_variantes = comando9_actual.get()
            subprocess.run(predecir_efecto_variantes, shell=True)
            barra.set(13)
            with open("./9.Efecto_variantes/efecto_variantes.tsv_summary.html") as archivo:
                raw_html = archivo.readlines()
                cadena = """""".join(raw_html)
            resultado_html_VEP.set(cadena)
            barra.set(18)
            procesar_tabla_VEP()
            barra.set(23)
            with open("./9.Efecto_variantes/tabla_efecto_variantes.html") as archivo2:
                raw_html2 = archivo2.readlines()
                cadena2 = """""".join(raw_html2)
            resultado_tabla_VEP.set(cadena2)
            barra.set(28)
            efecto_variantes_completado.set(True)

# 9. Renderizar el html con los resultados generales del comando 9
    @render.ui
    def html_VEP():
        return ui.HTML(resultado_html_VEP.get())
    
# 9. Renderizar el html con los resultados tabulados del comando 9
    @render.ui
    def tabla_VEP():
        return ui.HTML(resultado_tabla_VEP.get())
    
# 9. Compresión y descarga de los archivos generados con los comandos 9
    @render.download
    def descarga_resultados9():
        with zipfile.ZipFile("Resultados_prediccion_efecto_variantes.zip", "w") as archivozip:
            archivos_descarga = glob.glob("./9.Efecto_variantes/*")
            for archivo in archivos_descarga:
                archivozip.write(archivo)
        return "Resultados_prediccion_efecto_variantes.zip"

# 9. Activación del botón de siguiente del apartado 9 si se ha realizado el filtrado de variantes
    @reactive.effect
    def siguiente9():
        if efecto_variantes_completado.get() is True:
            ui.update_action_button("boton_siguiente9", disabled=False)

# 9. Paso del apartado 9 al resumen
    @reactive.effect
    @reactive.event(input.boton_siguiente9)
    def de9_a_10():
        ui.update_navs("panel", selected="Resumen")


#################### 10. Resumen ####################

##### Resumen Comandos #####

# 10. Texto de explicación del resumen
    @render.text
    def texto_resumen():
        return ui.HTML('En este apartado puede descargar todos los archivos generados hasta el momento, \
                       visualizar un resumen de todos los resultados obtenidos, un resumen de todos los comandos ejecutados \
                       y descargar un script con ellos para lanzarlo desde la terminal si desea replicar exactamente el mismo \
                       flujo de trabajo de forma automática.<br> <br>\
                       Tenga en cuenta que tanto los resultados como los comandos mostrados e incluídos en el script \
                       son los últimos que ha generado/ejecutado. Las opciones que tenga marcadas actualmente en los apartados \
                       no se reportarán aquí. De esta forma, se asegura la reproducibilidad del flujo de trabajo realizado. <br> <br>\
                       Puede acceder a cada uno de estos subapartados a partir de los siguientes desplegables.')

# 10. Texto cajas comandos
    @render.text
    def calidad_rc():
        if comando1_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando1_ejecutado.get()
    
    @render.text
    def limpieza_rc():
        if comando2_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando2_ejecutado.get()
    
    @render.text
    def indexado_rc():
        if comando3_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando3_ejecutado.get()

    @render.text
    def mapeo_rc():
        if comando4_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando4_ejecutado.get()
    
    @render.text
    def analisis_mapeo1_rc():
        if comando5b_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando5b_ejecutado.get()
    
    @render.text
    def analisis_mapeo2_rc():
        if comando5c_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando5c_ejecutado.get()
    
    @render.text
    def analisis_mapeo3_rc():
        if comando5_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando5_ejecutado.get()
    
    @render.text
    def analisis_mapeo4_rc():
        if comando5d_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando5d_ejecutado.get()
    
    @render.text
    def limpieza_duplicados1_rc():
        if comando6b_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando6b_ejecutado.get()
    
    @render.text
    def limpieza_duplicados2_rc():
        if comando6c_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando6c_ejecutado.get()
    
    @render.text
    def limpieza_duplicados3_rc():
        if comando6d_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando6d_ejecutado.get()
    
    @render.text
    def llamada_variantes1_rc():
        if comando7c_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando7c_ejecutado.get()
    
    @render.text
    def llamada_variantes2_rc():
        if comando7d_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando7d_ejecutado.get()
    
    @render.text
    def llamada_variantes3_rc():
        if comando7e_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando7e_ejecutado.get()
    
    @render.text
    def llamada_variantes4_rc():
        if comando7f_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando7f_ejecutado.get()
    
    @render.text
    def filtrado_variantes1_rc():
        if comando8_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando8_ejecutado.get()
    
    @render.text
    def filtrado_variantes2_rc():
        if comando8d_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando8d_ejecutado.get()
    
    @render.text
    def efecto_variantes_rc():
        if comando9_ejecutado.get() == "":
            return "No se ejecutó"
        else:
            return comando9_ejecutado.get()

##### Generación y descarga del script #####

# 10. Actualización automática del script
    @reactive.effect
    def actualizacion_script():
        comandos_ejecutados_html.set(f"#!/bin/bash <br>\
                                    <br>\
                                    {comando1a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando1_ejecutado.get()} <br>\
                                    <br>\
                                    {comando2a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando2b1_ejecutado.get()} <br>\
                                    <br>\
                                    {comando2b2_ejecutado.get()} <br>\
                                    <br>\
                                    {comando2_ejecutado.get()} <br>\
                                    <br>\
                                    {comando3a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando3b_ejecutado.get()} <br>\
                                    <br>\
                                    {comando3_ejecutado.get()} <br>\
                                    <br>\
                                    {comando4a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando4_ejecutado.get()} <br>\
                                    <br>\
                                    {comando5a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando5b_ejecutado.get()} <br>\
                                    <br>\
                                    {comando5c_ejecutado.get()} <br>\
                                    <br>\
                                    {comando5_ejecutado.get()} <br>\
                                    <br>\
                                    {comando5d_ejecutado.get()} <br>\
                                    <br>\
                                    {comando6a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando6b_ejecutado.get()} <br>\
                                    <br>\
                                    {comando6c_ejecutado.get()} <br>\
                                    <br>\
                                    {comando6d0_ejecutado.get()} <br>\
                                    <br>\
                                    {comando6d_ejecutado.get()} <br>\
                                    <br>\
                                    {comando7a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando7b_ejecutado.get()} <br>\
                                    <br>\
                                    {comando7c_ejecutado.get()} <br>\
                                    <br>\
                                    {comando7d_ejecutado.get()} <br>\
                                    <br>\
                                    {comando7e_ejecutado.get()} <br>\
                                    <br>\
                                    {comando7f_ejecutado.get()} <br>\
                                    <br>\
                                    {comando8a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando8b0_ejecutado.get()} <br>\
                                    <br>\
                                    {comando8b_ejecutado.get()} <br>\
                                    <br>\
                                    {comando8_ejecutado.get()} <br>\
                                    <br>\
                                    {comando8c_ejecutado.get()} <br>\
                                    <br>\
                                    {comando8d_ejecutado.get()} <br>\
                                    <br>\
                                    {comando9a_ejecutado.get()} <br>\
                                    <br>\
                                    {comando9_ejecutado.get()}")
        
        comandos_ejecutados_sh_txt.set(f"#!/bin/bash\n"
                                    f"\n"
                                    f"{comando1a_ejecutado.get()}\n"
                                    f"\n" 
                                    f"{comando1_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando2a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando2b1_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando2b2_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando2_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando3a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando3b_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando3_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando4a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando4_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando5a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando5b_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando5c_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando5_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando5d_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando6a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando6b_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando6c_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando6d0_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando6d_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando7a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando7b_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando7c_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando7d_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando7e_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando7f_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando8a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando8b0_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando8b_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando8_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando8c_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando8d_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando9a_ejecutado.get()}\n"
                                    f"\n"
                                    f"{comando9_ejecutado.get()}")

# 10. Caja del script
    @render.ui
    def script():
        return ui.HTML(comandos_ejecutados_html.get())

# 10. Descarga del script en .sh:
    @render.download
    def descarga_script_sh():
        with open("script_GenAgans.sh", "w") as script_sh:
            script_sh.write(comandos_ejecutados_sh_txt.get())
        return "script_GenAgans.sh"

# 10. Descarga del script en .txt:
    @render.download
    def descarga_script_txt():
        with open("script_GenAgans.txt", "w") as script_sh:
            script_sh.write(comandos_ejecutados_sh_txt.get())
        return "script_GenAgans.txt"

##### Resumen resultados #####

# 10. Cajas de resultados
    @render.ui
    def calidad_1_rr():
        return ui.HTML(resultado_html1_calidad.get())

    @render.ui
    def calidad_2_rr():
        return ui.HTML(resultado_html2_calidad.get())
    
    @render.ui
    def limpieza_rr():
        html2_limpio = limpiar_html(resultado_html_limpieza_lecturas.get(), "<head>", "</head>")
        return ui.HTML(html2_limpio)

    @render.ui
    def analisis_mapeo_rr():
        return ui.HTML(resultado_html_analisis_mapeo.get())
    
    @render.ui
    def duplicados_rr():
        return ui.HTML(resultado_txt_Duplicados.get())
    
    @render.ui
    def RG_rr():
        return ui.HTML(resultado_txt_ReadGroups.get())

    @render.ui
    def llamada_variantes_rr():
        return ui.HTML(resultado_txt_llamada_variantes.get())
    
    @render.ui
    def filtrado_variantes_rr():
        return ui.HTML(resultado_txt_filtrado_variantes.get())
    
    @render.ui
    def efecto_variantes_general_rr():
        return ui.HTML(resultado_html_VEP.get())
    
    @render.ui
    def efecto_variantes_tabla_rr():
        return ui.HTML(resultado_tabla_VEP.get())

##### Descarga de todos los archivos #####

# 10. Compresión y descarga de todos los archivos generados
    @render.download
    def descarga_todos_archivos():
        total_archivos = sum([len(archivos) for raiz, subcarpetas, archivos in os.walk("./") if archivos != "Archivos_generados.zip"])
        with ui.Progress(min=1, max=total_archivos) as barra:
            barra.set(message="Procesando...", detail="Dependiendo de la cantidad de archivos generados este proceso puede\
                                                        ser más o menos pesado. Espere, por favor.")
            conteo_barra = 1
            barra.set(conteo_barra)
            with zipfile.ZipFile("Archivos_generados.zip", "w") as archivozip:
                for raiz, subcarpetas, archivos in os.walk(ruta_archivos):
                    for archivo in archivos:
                        if archivo != "Archivos_generados.zip":
                            ruta_archivo = os.path.join(raiz, archivo)
                            archivozip.write(ruta_archivo, os.path.relpath(ruta_archivo, "./"))
                            conteo_barra += 1
                            barra.set(conteo_barra)
            barra.set(total_archivos)
        return "Archivos_generados.zip"


################################# Definición de la aplicación completa #################################
app = App(app_ui, server)
