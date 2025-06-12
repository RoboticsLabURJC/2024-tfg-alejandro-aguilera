---
title: Visualización de Dashboards
layout: single
permalink: /dashboards/
author_profile: true
---

## Gráfica 1: Ejercicios por Usuario
Este dashboard permite analizar la duración total que un usuario ha dedicado a cada ejercicio de la plataforma.

Para obtener esta información, el dashboard se conecta directamente a la base de datos **PostgreSQL** de *Unibotics*. Una vez establecida la conexión, la aplicación **Dash** ejecuta una consulta SQL parametrizada con el nombre de usuario introducido en el cuadro de texto.

La consulta SQL aprovecha la funcionalidad de **agrupación y agregación** de SQL: se filtran los registros por el usuario seleccionado y luego se agrupan por el identificador de ejercicio, calculando la suma de todos los tiempos asociados. La información se obtiene de la tabla `log_session`. La consulta que se ejecuta es:

`SELECT exercise, SUM(duration) as total_duration FROM public.log_exercises WHERE username = %s GROUP BY exercise HAVING SUM(duration) > 0 ORDER BY total_duration DESC;`

Esta consulta calcula la duración total (en segundos) acumulada para cada ejercicio realizado por el usuario indicado. La cláusula `GROUP BY` agrupa las filas que tienen el mismo valor de ejercicio y aplica la función agregada `SUM()` para sumar los datos de cada grupo.

En otras palabras, si el usuario ha realizado varias sesiones o intentos en un mismo ejercicio, todos esos tiempos se suman en un único resultado por ejercicio. Esta consulta retorna una tabla con dos columnas: el nombre de cada ejercicio y la suma de la duración total que el usuario ha invertido en él. Dichos resultados se cargan en un **DataFrame de Pandas** para su manipulación en la aplicación y posteriormente se emplean para generar la visualización.

Desde el punto de vista del usuario, este ve un **dashboard** y un cuadro de texto donde puede escribir el nombre del usuario que desea visualizar. Una vez introducido, el dashboard carga la información correspondiente.

El dashboard presenta los datos mediante un **gráfico horizontal de líneas con puntos**, también conocido como gráfico tipo **Lollipop**. Este tipo de visualización es una variación de un diagrama de barras: la barra tradicional se transforma en una línea delgada y el valor se resalta con un marcador circular al final.

Se eligió un gráfico del tipo *Lollipop* donde cada ejercicio aparece en función del tiempo total que el usuario le dedica, porque de esa manera es muy fácil ver de un vistazo en cuáles actividades pasa más tiempo. Al ordenar los ejercicios de mayor a menor duración, no se sigue el orden alfabético ni el listado original, sino que se muestran claramente las prioridades del usuario.

Esto permite observar, por ejemplo, que el ejercicio `global_navigation` ocupa la mayor parte de la sesión, mientras que `opticalflow_teleop` apenas consume unos minutos, sin necesidad de examinar cada número individualmente. Esta forma de presentar los datos facilita comparar tareas con duraciones muy distintas, sin confusiones ni búsquedas innecesarias.

## Conclusiones

- **Identificación de ejercicios más y menos trabajados:**  
  Las longitudes de las líneas revelan de un vistazo cuáles son los ejercicios en los que el usuario ha invertido más tiempo y cuáles menos.

- **Detección de patrones de esfuerzo o dificultad:**  
  Una duración total muy elevada en cierto ejercicio podría indicar que el usuario tuvo dificultades significativas o que necesitó múltiples intentos prolongados para completarlo. También podría reflejar que el ejercicio era extenso o que el usuario dedicó tiempo adicional explorando. Por el contrario, ejercicios con duraciones muy bajas pueden sugerir que el usuario los completó rápidamente o los abandonó pronto.

- **Distribución del tiempo de aprendizaje:**  
  El conjunto de todas las duraciones permite ver cómo el usuario ha distribuido su tiempo en la plataforma. Un perfil equilibrado mostraría duraciones similares entre ejercicios, mientras que un perfil más desequilibrado tendría unos pocos ejercicios dominando la mayor parte del tiempo total.

<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 2: Duración promedio de sesión por pais

Este dashboard tiene como objetivo mostrar la duración promedio de las sesiones de los usuarios de **Unibotics**, agrupadas por país. A través de un mapa mundial interactivo, se representa gráficamente qué países presentan una mayor o menor media de tiempo por sesión, permitiendo identificar patrones geográficos en el uso de la plataforma.

La información utilizada en este dashboard se obtiene desde la tabla `log_session`. La consulta SQL utilizada agrupa los datos por país, calcula la suma total de duración y el número total de sesiones por país. Posteriormente, se calcula en Python la duración promedio dividiendo ambos valores. La consulta es la siguiente:

`SELECT country, SUM(duration) AS total_duration, COUNT(*) AS session_count FROM public.log_session WHERE country IS NOT NULL AND duration > 0 GROUP BY country HAVING COUNT(*) > 0 ORDER BY total_duration DESC;`

A partir de esta consulta se genera un **DataFrame de Pandas** con el país y su respectiva duración promedio de sesión, que luego se utiliza para crear la visualización correspondiente. Este cálculo permite representar una métrica más equilibrada que la duración total y proporciona una mejor medida de cómo interactúan los usuarios con la plataforma en promedio.

El dashboard utiliza un **mapa coroplético**, generado mediante *Plotly Express*, en el que cada país se colorea en función de la duración promedio de sesión. Cuanto mayor es la duración, más intenso es el color asignado, siguiendo una escala cromática progresiva desde tonos claros hasta colores más saturados. Se utiliza una **paleta de colores continua personalizada**, diseñada para resaltar visualmente los valores extremos (puedes definir si prefieres, por ejemplo, `Viridis`, `Plasma`, `Turbo`, etc.).

Se eligió un mapa coroplético porque este tipo de visualización muestra de forma muy clara cómo se distribuye la duración total de sesiones a lo largo del mundo. Al asignar un color a cada país según su valor de duración, se puede identificar al instante qué regiones concentran más actividad y cuáles menos, sin necesidad de leer tablas o listas. El degradado de colores refuerza la percepción de diferencias entre países y también facilita ver patrones globales.

## Conclusiones

- **Alta duración promedio en España y Portugal:**  
  Esto indica que, en países como España y Portugal, las sesiones tienden a ser más largas, lo que refleja un uso más intensivo de la plataforma. No significa necesariamente que haya más sesiones en esos países, sino que, en promedio, los usuarios pasan más tiempo en cada sesión en comparación con otros lugares, donde el uso puede ser más breve o intermitente.

- **Bajas duraciones promedio en ciertos países:**  
  Podrían indicar una adopción más reciente, menor familiaridad con la plataforma o simplemente menos disponibilidad de tiempo por parte de los usuarios.

- **Utilidad para la administración de Unibotics:**  
  El dashboard permite identificar mercados con mayor impacto y uso sostenido, facilitando decisiones sobre soporte, localización de contenidos y planes de expansión, al tiempo que señala aquellas regiones donde el uso es bajo, lo que puede inspirar estrategias específicas de difusión, colaboración educativa o mejoras en el acceso a la plataforma.


<iframe src="{{ site.baseurl }}/assets/grafica2.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 3: Duración total de sesiones por pais
Este dashboard tiene como objetivo mostrar la duración total acumulada de todas las sesiones de usuarios de **Unibotics**, agrupadas por país. A través de un mapa interactivo, permite observar en qué regiones geográficas se ha registrado un mayor tiempo de uso en conjunto, proporcionando una visión global de la distribución de la actividad en la plataforma.

La información utilizada en este dashboard se obtiene desde la tabla `log_session`. La consulta SQL que se utiliza agrupa los datos por país y calcula la suma total de la duración de todas las sesiones correspondientes a cada país. La consulta es la siguiente:

`SELECT country, SUM(duration) as total_duration FROM public.log_session WHERE country IS NOT NULL GROUP BY country HAVING SUM(duration) > 0 ORDER BY total_duration DESC;`

A diferencia de otros dashboards que analizan promedios, en este caso se calcula simplemente la acumulación del tiempo total de uso de la plataforma por país. Esto permite identificar los países donde el uso absoluto de Unibotics ha sido más intenso.

Una vez obtenidos los resultados, se cargan en un **DataFrame de Pandas** con el país y su respectiva duración total de sesiones, y se utilizan como base para la representación gráfica en el mapa.

El dashboard utiliza un **mapa coroplético** (*choropleth map*), generado mediante *Plotly Express*, en el que cada país se colorea en función de la duración total de sesión. Cuanto mayor es la duración, más intenso es el color asignado, siguiendo una escala cromática progresiva desde tonos claros hasta colores más saturados. Se emplea una paleta de colores continua personalizada (por ejemplo, se puede utilizar `Viridis`, `Cividis` o una escala definida por el usuario) para resaltar visualmente los valores extremos.

Se eligió un mapa coroplético porque, al igual que en el caso del dashboard 1C, permite ver de un vistazo cómo se distribuye la duración total de sesiones por país: cada país se colorea según su valor, mostrando de forma inmediata qué regiones concentran más actividad y cuáles menos sin tener que depender de leer tablas o listas.

## Conclusiones

- **España destaca con el mayor volumen de tiempo total de sesiones:**  
  Esto refleja su fuerte implantación y uso intensivo de la plataforma, probablemente por ser el país de origen o principal mercado de Unibotics. Otros países europeos y latinoamericanos presentan niveles más bajos, lo que puede interpretarse como una menor penetración o un uso más reciente de la plataforma en esas regiones.

- **Diferencias geográficas claras:**  
  Algunos continentes como África o Asia presentan en general un uso más bajo, salvo excepciones, lo que podría señalar oportunidades de expansión o barreras de adopción actuales.

- **Utilidad para la gestión de Unibotics:**  
  Este dashboard permite identificar en qué países la plataforma tiene mayor presencia, lo que facilita la toma de decisiones estratégicas relacionadas con campañas, traducción de contenidos o inversiones para mejorar el servicio. También ayuda a detectar regiones con potencial para nuevas colaboraciones educativas. Por ejemplo, se observa un alto número de sesiones en Rumanía, lo cual podría ser una oportunidad para contactar con el equipo de gestión de Unibotics en ese país, entender cómo están trabajando allí y comparar el rendimiento de los usuarios con el de España. Este análisis comparativo puede proporcionar información valiosa para implementar mejoras en ambas regiones.


<iframe src="{{ site.baseurl }}/assets/grafica3.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 4: Sesiones por mes
Este dashboard muestra la evolución mensual del número de sesiones iniciadas en **Unibotics** a lo largo del año. Para ello, cuenta con un desplegable que permite seleccionar el año, actualizando automáticamente el gráfico. Además, diferencia entre usuarios masculinos y femeninos. El objetivo es analizar cómo varía el uso de la plataforma mes a mes y si existen diferencias significativas por género.

Los datos provienen de las tablas `log_session` y `common_user`. La consulta SQL utilizada realiza una agregación mensual teniendo en cuenta el total de sesiones iniciadas en cada mes, el número de sesiones realizadas por usuarias (género femenino) y el número de sesiones realizadas por usuarios (género masculino). La consulta utilizada es la siguiente:

`SELECT DATE_TRUNC('month', s.start_date) AS month, COUNT(*) AS total_sessions, COUNT(CASE WHEN u.gender = 'F' THEN 1 END) AS female_sessions, COUNT(CASE WHEN u.gender = 'M' THEN 1 END) AS male_sessions FROM public.log_session s JOIN public.common_user u ON s.username = u.username WHERE EXTRACT(YEAR FROM s.start_date) = %s GROUP BY month ORDER BY month;`

Una vez extraídos, los datos se procesan en **Pandas** para asegurar que los meses estén correctamente ordenados de enero a diciembre, y se formatea el nombre de los meses para facilitar la visualización.

El dashboard utiliza un **gráfico de líneas** para representar la evolución de las sesiones durante el año seleccionado. Se incluyen tres líneas: una para el total de sesiones (en azul), otra para sesiones femeninas (en rojo), y una tercera para sesiones masculinas (en verde). Cada punto en el gráfico representa el número de sesiones registradas ese mes para cada grupo.

Se eligió un gráfico de líneas con tres trazos (total, mujeres y hombres) porque permite visualizar de manera clara cómo evoluciona cada grupo a lo largo del tiempo. Al representar las líneas en el mismo gráfico, es fácil notar si en un mes ambos géneros aumentan al mismo tiempo o si uno de ellos se mantiene estable mientras el otro varía. Los colores diferenciados también ayudan a identificar visualmente los picos o caídas por categoría sin tener que revisar múltiples gráficos.

## Conclusiones

- **Más actividad en otoño:**  
  A partir de septiembre se nota un aumento claro en las sesiones, con el punto más alto en otoño. Esto coincide con el inicio del curso académico, cuando muchas personas retoman el uso de la plataforma.

- **Bajada en verano:**  
  En los meses de verano, especialmente en agosto, la actividad desciende notablemente. Es un período de vacaciones, y se observa una disminución en las conexiones, lo cual debe tenerse en cuenta al planificar campañas o recursos.

- **Inicio de año tranquilo:**  
  De enero a junio el uso de la plataforma es bastante estable, sin grandes fluctuaciones. Es una fase de ritmo más pausado pero constante.

- **Más sesiones de chicos que de chicas:**  
  A lo largo de todo el año se registran más sesiones por parte de usuarios masculinos que femeninos. Esto podría invitar a reflexionar sobre estrategias para incentivar una mayor participación femenina.

- **Utilidad para la gestión de Unibotics:**  
  Conocer estos patrones temporales y de género permite tomar decisiones más informadas, como cuándo lanzar campañas, en qué meses reforzar el soporte técnico o cómo organizar colaboraciones educativas para maximizar su impacto.


<iframe src="{{ site.baseurl }}/assets/grafica4.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 5: Frecuencia de usuario por duración
Este dashboard analiza cómo se distribuyen los usuarios de **Unibotics** según el tiempo total que han dedicado a un ejercicio específico. Utiliza una escala logarítmica para representar mejor las diferencias en las duraciones, ya que pueden ser muy grandes entre unos usuarios y otros.

Los datos provienen de las tablas `log_exercises` y `exercises`. El usuario cuenta con un desplegable que permite seleccionar un ejercicio concreto. Una vez seleccionado, se ejecuta una consulta SQL que suma el tiempo total que cada usuario ha dedicado a ese ejercicio. La consulta utilizada es la siguiente:

`SELECT username, SUM(duration) as total_duration FROM public.log_exercises WHERE exercise = %s GROUP BY username HAVING SUM(duration) > 0 ORDER BY total_duration;`

Después de obtener los datos, se aplica una **transformación logarítmica** al valor de duración total. Esto se hace para reducir la dispersión de los datos: dado que hay usuarios que pueden haber pasado desde unos pocos segundos hasta varias horas en un mismo ejercicio, el uso de una escala logarítmica permite representar toda la distribución de manera más equilibrada.

El dashboard utiliza un **histograma**, donde el eje horizontal representa el logaritmo de la duración total (en segundos) y el eje vertical representa el número de usuarios que tienen una duración dentro de cada rango.

Cada barra del histograma muestra cuántos usuarios se encuentran en ese intervalo de duración. Como las duraciones pueden estar muy concentradas en valores bajos y extenderse hacia valores mucho mayores, aplicar logaritmo en el eje X ayuda a comprimir la escala. Así se obtienen intervalos más balanceados que permiten apreciar mejor la distribución general de los usuarios.

Se eligió este tipo de gráfico porque permite visualizar fácilmente cómo se distribuyen las duraciones entre todos los usuarios en un ejercicio determinado. Al agrupar los tiempos en intervalos, es muy fácil identificar dónde se concentra la mayoría de la gente.

Este análisis permite detectar de un vistazo si la mayoría de los usuarios se sitúa en un tiempo intermedio o si hay grupos extremos que dedican muy poco o mucho tiempo. La forma del histograma revela de forma clara cómo se comportan los usuarios con ese ejercicio.

## Conclusiones

- **Distribución de los tiempos:**  
  Permite observar si la mayoría de los usuarios completan el ejercicio en tiempos similares o si existen grandes diferencias entre ellos.

- **Tiempos agrupados en valores bajos:**  
  Esto puede indicar que el ejercicio es sencillo o que muchos usuarios lo abandonaron rápidamente.

- **Gran variedad de tiempos:**  
  Sugiere que el ejercicio tiene un nivel de dificultad variable o permite enfoques diversos, lo cual lleva a dedicar más o menos tiempo dependiendo del usuario.

- **Utilidad para los profesores:**  
  Facilita detectar si el ejercicio está bien equilibrado en cuanto a dificultad, o si sería necesario hacer ajustes para mejorar la experiencia de aprendizaje.


<iframe src="{{ site.baseurl }}/assets/grafica5.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 6: Boxplot por usuario y ejercicio
Este dashboard muestra cómo se distribuye el tiempo que cada usuario ha dedicado a distintos ejercicios de **Unibotics**. Utiliza **diagramas de caja**, también conocidos como *boxplots*, y aplica una escala logarítmica para representar mejor las diferencias entre los usuarios.

Los datos se obtienen de la tabla `log_exercises`. Con la consulta SQL correspondiente se agrupa la información por nombre de ejercicio y por usuario, sumando la duración total que cada uno ha dedicado a cada ejercicio. Solo se consideran los casos donde el tiempo total registrado es mayor que cero. La consulta utilizada es:

`SELECT exercise, username, SUM(duration) as total_duration FROM public.log_exercises WHERE duration > 0 GROUP BY exercise, username HAVING SUM(duration) > 0 ORDER BY exercise;`

Una vez extraídos los datos, se calcula el **logaritmo de la duración total** para cada usuario. Esta transformación se realiza para normalizar los valores, ya que algunos usuarios pueden tener tiempos muy pequeños y otros muy grandes, y la escala logarítmica permite visualizar mejor esa variabilidad.

En el dashboard, cada ejercicio se representa en el eje horizontal, mientras que en el eje vertical se muestra el logaritmo del tiempo total invertido por los usuarios. Para cada ejercicio, el boxplot muestra:

- La **mediana de las duraciones**, que aparece como una línea en el centro de la caja.
- El **rango intercuartílico**, representado por el tamaño de la caja, que abarca el 50% central de los usuarios.
- Los **valores extremos o atípicos**, que se visualizan como puntos dispersos fuera de la caja.

Gracias a este tipo de gráfico es posible visualizar de forma clara cómo varía la dedicación de los usuarios en cada ejercicio, y detectar si hay muchos usuarios que dedican tiempos muy distintos o si la mayoría se concentra en valores similares. Además, se muestran todos los puntos individuales sobre los diagramas, lo que permite ver la dispersión real de los datos con mayor precisión.

Este dashboard permite **comparar rápidamente el comportamiento de los usuarios en cada ejercicio**. A partir de los datos, se pueden destacar los siguientes puntos importantes:

- **Uniformidad en el tiempo dedicado:**  
  Permite observar si la mayoría de los alumnos invierten un tiempo similar o si existen grandes diferencias entre ellos.

- **Ejercicios con tiempos elevados:**  
  Identifica aquellos en los que algunos usuarios dedican mucho más tiempo, lo que podría indicar mayor dificultad o especial interés.

- **Casos extremos:**  
  Detecta actividades con muchas diferencias marcadas en los tiempos, lo que puede señalar problemas en el planteamiento o una dificultad muy variable entre estudiantes.

- **Información para los profesores:**  
  Ayuda a identificar ejercicios que podrían requerir cambios o mejoras para optimizar la experiencia de aprendizaje.

- **Orientación para diseñadores de contenidos:**  
  Facilita evaluar si los ejercicios generan el trabajo esperado o si convendría añadir ayudas o dividir las actividades en partes más manejables.

<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 7: Boxplot por ejercicio

El dashboard 3C es muy similar al dashboard 3B, ya que también utiliza **diagramas de caja** (*boxplots*) para representar los datos, pero con una diferencia importante: en lugar de analizar el tiempo total que cada usuario dedica a un ejercicio, aquí se analiza la **duración de cada sesión individual**.

Mientras que en el dashboard anterior se sumaban todas las sesiones de un usuario para un ejercicio determinado, en este caso se estudia cada sesión por separado, sin agruparlas. Al igual que antes, se aplica una **escala logarítmica** para representar mejor las diferencias en los tiempos, ya que algunas sesiones pueden durar solo unos pocos segundos y otras mucho más.

Para obtener estos datos se utiliza una consulta SQL que selecciona, para cada registro de sesión, el nombre del ejercicio y la duración de esa sesión concreta. La consulta es la siguiente:

`SELECT exercise, duration FROM public.log_exercises WHERE duration > 0 ORDER BY exercise;`

El objetivo del dashboard es ofrecer una **visión más detallada** sobre cómo varía el tiempo de trabajo en cada intento o sesión específica, algo que no era visible en el dashboard 3B, donde solo se mostraba el esfuerzo acumulado por usuario. Aquí es posible detectar, por ejemplo, si un ejercicio tiene sesiones generalmente cortas o si hay mucha variación entre los intentos de distintos usuarios.

En este dashboard, cada ejercicio se representa en el eje horizontal, y en el eje vertical se muestra el **logaritmo de la duración** de cada sesión. El boxplot de cada ejercicio incluye:

- La **mediana** de las duraciones por sesión.
- El **rango intercuartílico**, que contiene el 50% central de las sesiones.
- Los **valores atípicos**, mostrados como puntos fuera de la caja, que indican sesiones especialmente largas o cortas.

Esta representación es útil para entender mejor el comportamiento real de los usuarios dentro de cada ejercicio. Permite ver si los estudiantes tienden a resolver los ejercicios rápidamente o si, por el contrario, dedican mucho tiempo en intentos sucesivos. También puede ayudar a identificar ejercicios con **alta dispersión en la duración por sesión**, lo que puede ser una pista sobre su dificultad o sobre la necesidad de mejorar su planteamiento o instrucciones.

Este dashboard aporta información complementaria a la que ofrece el 3B y permite a docentes y diseñadores tomar decisiones más precisas en relación con la estructura de los ejercicios y la experiencia de usuario en la plataforma.


<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

