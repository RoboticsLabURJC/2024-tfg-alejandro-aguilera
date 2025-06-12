---
title: Visualización de Dashboards
layout: single
permalink: /dashboards/
author_profile: true
---

## Gráfica 1: Ejercicios por Usuario
El dashboard **1A** permite analizar la duración total que un usuario ha dedicado a cada ejercicio de la plataforma.

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
texto.

<iframe src="{{ site.baseurl }}/assets/grafica2.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 3: Duración total de sesiones por pais
Este gráfico compara el rendimiento del usuario según distintas categorías de ejercicios, como percepción o coordinación.

<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 4: Sesiones por mes
Representa la duración media por ejercicio, útil para detectar ejercicios que requieren más esfuerzo o atención.

<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 5: Frecuencia de usuario por duración
Analiza cómo ha cambiado la actividad del usuario cada semana, mostrando progresos o bajones en la práctica.

<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 6: Boxplot por usuario y ejercicio
En esta gráfica se puede observar cómo se compara un usuario respecto a otros en términos de duración o frecuencia.

<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

---

## Gráfica 7: Boxplot por ejercicio
Visualiza en qué horas del día suele estar activo el usuario, ideal para adaptar sesiones a momentos más productivos.

<iframe src="{{ site.baseurl }}/assets/grafica1.html" width="100%" height="600px" frameborder="0"></iframe>

