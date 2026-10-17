<div align="center">

<img alt="TREND-PREDICTOR: proyectá las restricciones de las que depende tu proyecto a 5 y 10 años y mirá cuándo se vuelve factible" src="../assets/banner.svg" width="100%">

<br>

**Skill para agentes que proyecta a 5 y 10 años las restricciones de las que depende un proyecto,<br>y te dice qué tan probable es que sea factible, qué lo va a frenar y cuándo empezar a construirlo.**

[English](../README.md) | **Español** | [简体中文](README_cn.md)

[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-2F6FB5?style=flat-square&labelColor=111111)](../LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-8DB8E3?style=flat-square&labelColor=111111)](../skills/trend-predictor/scripts/trend_predictor.py)

[Inicio rápido](#inicio-rápido) · [Cómo funciona](#cómo-funciona) · [Pruebas](#qué-tan-bien-funciona) · [Instalación](#instalación) · [Uso](#uso) · [Límites](#límites) · [Preguntas](#preguntas-frecuentes)

</div>

---

## Inicio rápido

```bash
npx skills add qaemu/trend-predictor-skill
```

O agregalo a mano en Claude Code, desde el marketplace de plugins:

```text
/plugin marketplace add qaemu/trend-predictor-skill
/plugin install trend-predictor@trend-predictor
```

> [!NOTE]
> TREND-PREDICTOR da probabilidades, no profecías. Cada resultado es condicional ("61% para 2035 *si* sigue la tendencia 2010–2025") y queda escrito como una afirmación con fecha que podés verificar después.

## Funciona mejor con PARADIGMA

TREND-PREDICTOR es la mitad que mira hacia adelante de un par. [**PARADIGMA**](https://github.com/qaemu/paradigma-skill) mira hacia atrás: qué restricciones de un campo cayeron en los últimos años, quién está construyendo sobre cada una y dónde quedan huecos abiertos. TREND-PREDICTOR mira hacia adelante: ¿un proyecto concreto se va a volver factible a medida que esas restricciones sigan moviéndose?

**Instalá PARADIGMA también.** Corrélo primero sobre tu campo y después corré TREND-PREDICTOR sobre el proyecto que estás evaluando:

```bash
npx skills add qaemu/paradigma-skill
```

- Los dos usan los mismos archivos de datos (`points.csv`, `constraints.csv`, `noncost.csv`), así que una corrida de PARADIGMA te adelanta trabajo: TREND-PREDICTOR reutiliza sus datos con fuente en vez de juntarlos de nuevo.
- PARADIGMA (v0.4.2 en adelante) guarda los datos más viejos que encuentra en `out_of_window.csv`. Pronosticar necesita 10 años o más de historia, así que esos puntos viejos acá importan.
- PARADIGMA te dice **qué** restricciones importan; TREND-PREDICTOR junta historia más densa solo para las 3–5 de las que depende tu proyecto.

## Por qué pronosticar restricciones

Un proyecto es factible cuando aquello de lo que depende es lo bastante barato, lo bastante bueno y está permitido: actuadores por debajo de un costo objetivo, una batería por encima de una densidad de energía objetivo, una norma vigente, una patente vencida. Esas cosas se mueven según tendencias medibles, y la investigación sobre pronóstico tecnológico es clara sobre qué funciona:

- **La propia tendencia histórica de una tecnología, extendida con rangos de error honestos, le gana a los paneles de expertos** en costo y prestaciones hasta unos 10 años ([Farmer & Lafond 2016](https://arxiv.org/abs/1502.05274); [Meng et al. 2021](https://www.cmcc.it/article/recent-technology-cost-forecasts-underestimate-the-pace-of-technological-change)). Los expertos y los grandes modelos institucionales fueron sistemáticamente demasiado pesimistas: los modelos esperaban que el costo solar bajara 2,6% por año en 2010–2020, y bajó cerca de 15%.
- **Los anuncios exageran.** Alrededor del 11% de la capacidad de hidrógeno anunciada para 2030 tenía decisión final de inversión (IEA, 2025).
- **Llegar demasiado temprano se ve igual que equivocarse.** Saber *cuándo* una restricción debería cruzar tu umbral importa tanto como saber *si* lo va a cruzar.

| Es | No es |
|---|---|
| Una probabilidad por requisito y horizonte, calculada en código | Una adivinanza escrita en prosa |
| Rangos probados sobre la propia historia de cada serie antes de confiar en ellos | Líneas rectas dibujadas hacia el futuro |
| Explícito sobre qué números son supuestos de criterio | Una precisión que no tiene |
| Una lista de predicciones con fecha, verificables | Una opinión de una sola vez |

## Cómo funciona

<img alt="Ocho pasos: requisitos, historia, prueba retrospectiva, pronóstico, eventos con fecha, madurez, puntaje, verificación e informe" src="../assets/pipeline.svg" width="100%">

| Paso | Qué pasa |
|---|---|
| **1. Requisitos** | Descompone el proyecto en lo que tiene que ser cierto: **metas** de costo o prestaciones derivadas de la economía unitaria, **eventos** con fecha (leyes, vencimientos de patentes, fábricas), pasos de **madurez** (TRL) y temas de **criterio** respaldados por pronósticos colectivos o encuestas publicadas. Nombra la restricción que cambió hace poco, o marca el riesgo de "demasiado temprano". |
| **2. Historia** | Agentes auxiliares juntan 10 años o más por curva, cada punto con su enlace, una línea de producto por serie. Reutiliza los datos de PARADIGMA cuando existen. |
| **3. Prueba retrospectiva** | Antes de confiar en una serie, el motor la pronostica desde cada año pasado y mide cuántas veces la realidad cayó dentro de sus rangos. |
| **4. Pronóstico** | Rangos calibrados (paseo aleatorio con deriva de Farmer–Lafond, t de Student). Reparaciones automáticas para productos mezclados, valores atípicos, cambios de tendencia y límites físicos, cada una elegida con una prueba explícita. A las series que siguen demasiado ruidosas se les manda un agente a buscar datos más densos. |
| **5. Eventos con fecha** | Leyes con fecha de entrada en vigencia, vencimientos de patentes, normas, fábricas anunciadas, cada uno descontado según su estado (anunciado, decisión final de inversión, en construcción). |
| **6. Madurez** | Pasos de madurez tecnológica con evidencia, y datos de criterio de Metaculus, Manifold o consultas a expertos publicadas. |
| **7. Puntaje** | Probabilidad de que cada requisito se cumpla a +5 y +10 años, la probabilidad conjunta junto al **eslabón más débil**, un veredicto, sensibilidad, un pre-mortem y la **ventana de inicio**: el año en que conviene empezar a construir, según tu tiempo de desarrollo. |
| **8. Verificación + informe** | Un agente nuevo, que no hizo nada de la investigación, vuelve a abrir cada fuente. Informe, gráficos de abanico, planilla y un registro de predicciones para evaluar más adelante. |

### Reglas básicas

1. **Cada número tiene un enlace.** Lo que falta se informa como faltante, nunca se estima.
2. **Las cuentas se hacen en código** ([`trend_predictor.py`](../skills/trend-predictor/scripts/trend_predictor.py)), nunca las hace el modelo.
3. **Primero se prueba el método sobre los datos.** Ninguna serie es confiable hasta que corrió su prueba retrospectiva.
4. **El eslabón más débil se informa junto a la probabilidad conjunta.** Un proyecto no puede rendir más que su peor requisito.
5. **Cada resultado se escribe como una predicción con fecha y verificable**, para que corridas futuras puedan evaluar las anteriores.

## Qué obtenés

<div align="center">
<img alt="Gráfico de factibilidad: probabilidad de que cada requisito se cumpla a +5 y +10 años, eslabón más débil y veredicto" src="../assets/feasibility.svg" width="78%">
<br>
<sub>Ilustración del gráfico de factibilidad. Una corrida real puntúa los requisitos de tu proyecto.</sub>
</div>

<br>

| Veredicto | Regla |
|---|---|
| **Probablemente factible** | Requisito más débil ≥ 80% y conjunta ≥ 60% |
| **Plausible** | Conjunta ≥ 35% |
| **Apuesta lejana** | Conjunta ≥ 12% |
| **Improbable** | Conjunta < 12% |
| **Incierto** | Reemplaza a los anteriores cuando el requisito más débil se apoya en evidencia débil: una curva de grado C/D, o una probabilidad estimada por los propios agentes de la corrida. El puntaje se conserva como "si los datos se sostienen" |

**Entregables**

- **Informe.** Primero el veredicto por horizonte, con el eslabón más débil, la ventana de inicio y lo único que hay que vigilar. Después una ficha por requisito (meta y cómo se derivó, gráfico de abanico, tendencia, resultado de la calibración, reparaciones aplicadas, probabilidad por horizonte), una línea de tiempo de eventos con fecha, madurez, un pre-mortem, señales a vigilar con fecha de revisión, y método, confianza y fuentes.
- **Planilla (.xlsx).** Abre en **Start here**, que explica cada término en palabras simples, y después el puntaje del proyecto, las probabilidades de cada requisito, los ajustes de cada serie, los rangos del pronóstico, la calibración, los eventos, las señales, el registro de predicciones y cada dato con su enlace.
- **Gráficos.** Un gráfico de abanico por curva (historia, pronóstico mediano, rangos del 50/80/95%, meta, límites) y el gráfico de factibilidad.

## Qué tan bien funciona

Cada conjunto de pruebas corre sin conexión, y su salida está guardada en [`tests/results/`](../tests/results/SUMMARY.md).

| Conjunto | Qué prueba | Resultado |
|---|---|---|
| [`test_engine`](../tests/results/test_engine.txt) | Calibración en 60 tecnologías simuladas; pronóstico, factibilidad, gráficos y planilla de punta a punta | 13 / 13 |
| [`test_edge_cases`](../tests/results/test_edge_cases.txt) | Inflación, filas malas, formatos de fecha mezclados, huecos, límites físicos, productos mezclados, archivos faltantes, ajustes manuales, la regla del veredicto incierto | 39 / 39 |
| [`test_autofix`](../tests/results/test_autofix.txt) | Las reparaciones automáticas no molestan con datos limpios y ayudan ante cambios de tendencia y valores atípicos reales | 7 / 7 |
| [`test_real_data`](../tests/results/test_real_data.txt) | Prueba retrospectiva con datos reales y con fuente | 12 / 12 |
| [`test_real_run`](../tests/results/test_real_run.txt) | Repuntúa una corrida real hecha por un modelo gratuito (MiMo V2.6 Flash): probabilidades reproducidas exactas, los veredictos con evidencia débil pasan a Incierto | 23 / 23 |

Lo que dicen los números, sin maquillaje:

- **Calibración.** En tecnologías simuladas, los rangos del 80% contienen el 77% de los resultados y los del 95%, el 93%. Casi honesto, apenas angosto.
- **Reparaciones.** Con datos limpios se activan en el 1–3% de las series y no cambian la precisión. Ante una desaceleración real se activan en cerca de la mitad de los casos y bajan el error del pronóstico entre 20 y 37%. Cuando la desaceleración está tapada por mucho ruido, casi nunca se activan, porque los datos no la distinguen del azar.
- **Datos reales** ([ejemplo](../examples/backtest-predictive-maintenance)): los pronósticos de salarios hechos desde 2013–2017 quedaron a un 3% de lo que pasó. Los hechos desde 2019 fallaron en 2020–2023, cuando el salto del COVID y después la inflación movieron los salarios reales. Un rango del 80% debería fallar más o menos 1 de cada 5 veces, y ningún modelo de tendencia anticipa un shock. Con precios de lanzamiento de GPU ruidosos y una serie de cámaras térmicas que mezcla tipos de producto, el motor se niega con razón a dar un pronóstico informativo a 10 años y pide datos más densos.

## Ejemplos

**Una corrida real con un modelo gratuito.** [`examples/mimo-scan-swe-salaries`](../examples/mimo-scan-swe-salaries) es un escaneo completo de salarios de ingeniería de software en EE. UU. hecho por MiMo V2.6 Flash en OpenCode, con su revisión. La recolección de datos y la verificación se sostuvieron (92% de 84 controles coincidieron). Dos de sus tres veredictos de proyecto se apoyaban en probabilidades inventadas por sus propios agentes, y citó una calibración mejor que la de sus propios archivos. Ahora el motor marca esos veredictos como Inciertos, y las instrucciones exigen citar la calibración tal cual.

**Una prueba retrospectiva.** Hay una prueba retrospectiva con los datos con fuente de la corrida de mantenimiento predictivo de PARADIGMA en [`examples/backtest-predictive-maintenance`](../examples/backtest-predictive-maintenance). Se para en 2013, 2015, 2017 y 2019, pronostica solo con los datos disponibles en ese momento y compara con lo que pasó de verdad. Cada pronóstico, rango y error está en `output/backtest.csv`.

## Instalación

TREND-PREDICTOR sigue el formato abierto [Agent Skills](https://agentskills.io): un `SKILL.md` más un motor en Python. Lo puede usar cualquier agente que navegue la web, corra Python e, idealmente, lance agentes auxiliares.

### Cualquier agente (skills CLI)

```bash
npx skills add qaemu/trend-predictor-skill                    # proyecto actual
npx skills add qaemu/trend-predictor-skill -g                 # todos los proyectos
npx skills add qaemu/trend-predictor-skill -a claude-code -a opencode
```

Usa el [skills CLI](https://github.com/vercel-labs/skills), compatible con Claude Code, OpenCode, Codex, Cursor y muchos más. Agregá `qaemu/paradigma-skill` de la misma forma.

### Claude Code

Como plugin, que te da actualizaciones con `/plugin`:

```text
/plugin marketplace add qaemu/trend-predictor-skill
/plugin install trend-predictor@trend-predictor
```

Las skills de plugins llevan prefijo, así que se corre como `/trend-predictor:trend-predictor "<proyecto>"`.

O como skill personal, que se corre como `/trend-predictor "<proyecto>"`:

```bash
git clone https://github.com/qaemu/trend-predictor-skill.git
mkdir -p ~/.claude/skills && cp -r trend-predictor-skill/skills/trend-predictor ~/.claude/skills/
```

### Apps de Claude (web, escritorio, móvil)

1. Descargá [`dist/trend-predictor.zip`](../dist/trend-predictor.zip). Contiene la carpeta `trend-predictor` con `SKILL.md` y el motor.
2. Activá **Code execution and file creation** en **Settings → Capabilities**.
3. Andá a **Customize → Skills**, hacé clic en **+**, después **Create skill → Upload a skill**, y elegí el ZIP.

Guía de Anthropic: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### OpenCode

```bash
git clone https://github.com/qaemu/trend-predictor-skill.git
mkdir -p ~/.config/opencode/skills && cp -r trend-predictor-skill/skills/trend-predictor ~/.config/opencode/skills/
```

OpenCode también lee `~/.claude/skills/`, así que una instalación de Claude Code también sirve ahí. Primero fijate que la búsqueda web funcione con tu proveedor. Sin eso, la skill no puede juntar datos.

### Requisitos

| Necesita | Para qué |
|---|---|
| Búsqueda web y lectura de páginas | Cada número sale de una fuente |
| Python 3.10+ con `pandas`, `numpy`, `matplotlib`, `openpyxl` (`scipy` recomendado) | El motor, sus gráficos y la planilla de Excel. `scipy` da rangos t de Student exactos |
| Agentes auxiliares (opcional) | Investigación en paralelo y la verificación independiente. Sin ellos corre de a un paso y marca la verificación como propia |

## Uso

```text
/trend-predictor "<proyecto>" [campo] [región] [horizontes] [standard|deep]
/trend-predictor scan "<campo>" [región] [horizontes]
```

| Argumento | Por defecto | Notas |
|---|---|---|
| `proyecto` | obligatorio | Qué entrega, a quién y a qué precio. Si es demasiado vago para fijar metas, la skill pregunta una vez |
| `scan` | — | En lugar de un proyecto: qué umbrales de un campo es más probable que se crucen, convertidos en 3–5 proyectos candidatos y puntuados |
| `campo` | se deduce | Se usa para encontrar una corrida de PARADIGMA que reutilizar |
| `región` | global | Indica dónde los datos están centrados en EE. UU. o la UE |
| `horizontes` | `5,10` | Años después del último año completo. Se admite de 1 a 15; más allá de 10 el resultado son escenarios, no pronósticos |

```text
/trend-predictor "robot doméstico que dobla ropa por menos de US$2.000" robótica global
/trend-predictor "cámara de frío solar para pequeños productores" agro "América Latina"
/trend-predictor scan "almacenamiento de energía en red" global 5,10
```

> [!IMPORTANT]
> Una corrida completa junta historia con fuente usando varios agentes en paralelo y consume una parte importante del uso de un plan. Usala para una idea que estés evaluando en serio, no para hacer lluvia de ideas.

## Con qué modelo correrlo

Lo que importa es la disciplina con las fuentes y seguir el procedimiento durante una corrida larga.

| Rol | Recomendado | Esfuerzo |
|---|---|---|
| Corrida principal (requisitos, puntaje, informe) | Claude Opus 5.5 | alto |
| Auxiliares de recolección de datos | Claude Sonnet 5.5 | medio–alto |
| Verificación independiente | Opus 5.5 | alto |

Para probar cualquier modelo, correlo sobre 3 curvas con datos bien publicados, como precios de packs de ion-litio y de módulos solares, y abrí cada enlace que devuelva. **Si inventa aunque sea un enlace o un número, no sirve.**

## Las cuentas

<details>
<summary><b>Cómo se pronostica una curva</b></summary>

<br>

1. **Normalizar.** Valores por unidad de prestación, en dólares constantes (IPC de EE. UU. de FRED). Los valores en otras monedas necesitan un tipo de cambio citado.
2. **Valor anual.** La mediana de los puntos de cada año o, cuando una serie mezcla productos, el mejor valor disponible hasta ese momento (la frontera precio-prestación).
3. **Ajuste** ([Farmer & Lafond 2016](https://arxiv.org/abs/1502.05274)). El logaritmo del valor es un paseo aleatorio con deriva: deriva = (último − primero) / años; volatilidad K a partir de los cambios anuales, con los huecos escalados por √Δt.
4. **Rangos.** Mediana = último valor + deriva × τ. Dispersión = K·√(A*/(1+θ²)) con A* = −2θ + (1 + 2(m−1)θ/m + θ²)(τ + τ²/m), θ = 0,63, cuantiles t de Student con m−1 grados de libertad.
5. **Probabilidad.** P(que el valor sea al menos tan bueno como la meta en el año Y), directo de la distribución del pronóstico. Una meta más allá de un límite físico da 0.
6. **Ensanche a largo plazo.** Pasados los 5 años, los rangos de tecnologías físicas se ensanchan hasta un 40% a los 10 años, porque los pronósticos de largo plazo de tecnologías físicas fallan más que los de tecnologías de la información.

</details>

<details>
<summary><b>Las reparaciones automáticas</b></summary>

<br>

| Problema | Prueba | Reparación |
|---|---|---|
| Productos mezclados | Valores del mismo año que difieren más de 3× | Mejor valor disponible hasta ese momento (frontera) |
| Valores atípicos | Un cambio anual a más de 5,5 desvíos robustos del típico | Tendencia (Theil–Sen) y volatilidad (MAD) robustas |
| Cambió la tendencia | Deriva de los últimos 15/10/8 años contra la anterior, z > 3,2 con errores de Farmer–Lafond | Ajuste sobre la ventana reciente |
| Límite físico | La tendencia recta cruza un piso o techo con fuente dentro del horizonte | Modelar la distancia que falta hasta el límite, para que el avance se frene cerca de él |

Las reparaciones se eligen con pruebas explícitas, no probando muchos ajustes y quedándose con el mejor. Una versión anterior hacía eso último; parecía mejor con datos reales y era peor con datos simulados limpios, porque estaba ajustando ruido.

</details>

<details>
<summary><b>Supuestos de criterio (marcados en cada informe)</b></summary>

<br>

| Supuesto | Valor | Por qué es de criterio |
|---|---|---|
| Probabilidades de eventos (a la fecha / dentro de 3 años) | Patente otorgada 0,90/0,97 · norma sancionada 0,75/0,92, propuesta 0,30/0,55 · capacidad anunciada 0,25/0,45, decisión final de inversión 0,60/0,85, en construcción 0,75/0,92 | Hay pocas tasas base medidas; los valores de capacidad se apoyan en los proyectos de hidrógeno y baterías |
| Madurez | Años medianos por paso de TRL: software 0,6, electrónica 1,3, hardware 2,0, energía 2,5, infraestructura 3,0 | La evidencia sobre tiempos entre TRL es escasa (el GPS tardó 11,7 años de TRL 3 a 9) |
| Ensanche | Dominios físicos: dispersión × (1 + 0,4·(h−5)/5) pasados los 5 años | La dirección está documentada, el tamaño no |

</details>

<details>
<summary><b>Correr el motor solo</b></summary>

<br>

```bash
cd skills/trend-predictor/scripts
python3 trend_predictor.py cpi                                   # promedios anuales del IPC de EE. UU. desde FRED
python3 trend_predictor.py hindcast --end 2025                   # points.csv -> hindcast.csv, calibration.csv
python3 trend_predictor.py forecast --end 2025 --plots           # -> series_fit.csv, forecasts.csv, plots/
python3 trend_predictor.py feasibility --end 2025 --lead-years 2 --plots   # requirements.csv -> puntaje del proyecto
python3 trend_predictor.py workbook --project "…" --end 2025 --date 2026-10-16
```

Los esquemas de los CSV están en [`SKILL.md`, Appendix B](../skills/trend-predictor/SKILL.md#appendix-b-csv-schemas).

</details>

## Fuentes de datos

Todas las fuentes son gratuitas. El informe indica dónde agregarían más las bases pagas.

| Necesidad | Usa (gratis) | Lo que agregan los profesionales (pago) |
|---|---|---|
| Historia de costo y prestaciones | Our World in Data, Santa Fe Performance Curve Database, Epoch AI, BLS / FRED, USGS, NREL, IEA, NHGRI, papers de curvas de aprendizaje, listas de precios + Wayback Machine | BloombergNEF, firmas de desarme técnico (teardown) |
| Eventos con fecha | Boletines oficiales (Federal Register, EUR-Lex, boletines nacionales), Google Patents, Lens.org, ISO / IEC / IEEE | Seguimiento legal y de patentes |
| Datos de criterio | Metaculus, Manifold, Good Judgment Open, consultas a expertos publicadas | Paneles de expertos por encargo |

## Límites

- **Hasta 10 años.** Los rangos están validados hasta unos 10–11 años. Más allá, el resultado son escenarios.
- **No pronostica la adopción.** La skill evalúa si un proyecto se vuelve *factible*, no qué tan rápido lo va a comprar la gente. Ningún método pronostica bien los tiempos de adopción; la única medición son clientes reales.
- **Necesita datos.** Las series con menos de 5 cambios anuales no reciben pronóstico, y las ruidosas se informan como no informativas. La mayoría de los campos tienen pocas series largas y buenas.
- **No anticipa shocks.** Una pandemia, una guerra o un cambio de política repentino sacan los valores de los rangos. Los rangos cubren sorpresas típicas, no todas.
- **Algunos números son de criterio.** Los supuestos de eventos, madurez y ensanche están marcados y se pueden ajustar.
- **Estado: v0.2, experimental.** Probado con datos simulados, una prueba retrospectiva real y una corrida real completa (con un modelo gratuito), publicada con su revisión.

## Preguntas frecuentes

**¿Toca mis archivos o cuentas?**
No. Lee sitios web públicos y escribe solo en su propia carpeta de trabajo.

**¿Por qué no preguntarle directamente a un modelo cuándo algo va a ser factible?**
Porque te va a dar una fecha con mucha seguridad, y no vas a poder saber en qué se basa. Esta skill exige una fuente para cada número, hace las cuentas en código, prueba su propio método sobre la historia de cada serie y escribe cada afirmación para que se pueda verificar después.

**¿En qué se diferencia de PARADIGMA?**
PARADIGMA mapea lo que ya cambió en un campo y quién está construyendo sobre eso. TREND-PREDICTOR puntúa las chances de un proyecto en fechas futuras. Corré PARADIGMA primero para saber dónde mirar, y después TREND-PREDICTOR sobre lo que construirías ahí.

**¿Puedo confiar en una probabilidad a 10 años?**
Como ranking y control de cordura, sí. Como número preciso, no: tomá 61% como "más probable que no, si las tendencias se mantienen", y vigilá las señales que te da el informe.

## Repositorio

```text
trend-predictor-skill/
├── .claude-plugin/              manifiestos de marketplace y plugin de Claude Code
├── skills/trend-predictor/
│   ├── SKILL.md                 instrucciones que sigue el agente
│   └── scripts/trend_predictor.py   motor (cpi, hindcast, forecast, feasibility, workbook)
├── tests/                       cuatro conjuntos sin conexión + run_all.sh
│   └── results/                 salida guardada de la última corrida (SUMMARY.md)
├── examples/                    prueba retrospectiva con datos reales + una corrida real revisada con un modelo gratuito
├── docs/research.md             la investigación detrás del método, con fuentes
├── dist/trend-predictor.zip     skill lista para subir a las apps de Claude (tools/package.sh)
├── tools/                       make_assets.py (gráficos del README), package.sh (rearma el ZIP)
├── README/                      traducciones de esta página
└── assets/                      banner, pasos y gráfico de factibilidad
```

```bash
./tests/run_all.sh   # corre todos los conjuntos y reescribe tests/results/
```

## Contribuir

Issues y pull requests son bienvenidos, sobre todo:

- corridas reales que quieras compartir en `examples/`, idealmente con resultados que se puedan verificar más adelante
- series de datos largas, limpias y gratuitas para una tecnología concreta
- mejores tasas base para los supuestos de criterio (demoras de eventos, tiempos entre TRL)

Mantené las reglas: cada número lleva su fuente y todas las cuentas quedan en el motor.

## Licencia

[MIT](../LICENSE) © 2026 qaemu

<div align="center">
<br>
<sub>Hecho por <a href="https://github.com/qaemu">qaemu</a>. Del mismo autor: <a href="https://github.com/qaemu/paradigma-skill">PARADIGMA</a>, el panorama de cambios de restricciones sobre el que se apoya esta skill, y <a href="https://github.com/qaemu/phasentic">Phasentic</a>, identificación de fases por difracción de rayos X en polvo, de código abierto.</sub>
</div>
