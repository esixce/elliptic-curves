# Enseñanza ECC — Notas del Presentador

Solo puntos clave. Abre el cuaderno correspondiente, ejecuta celdas en vivo, habla desde estas notas.

---

## 00-intro.ipynb (~5 min)

**Abre con el problema, no con las matemáticas.**

- "Bitcoin es un libro contable público. Todos pueden leer cada transacción."
- Dos problemas a resolver:
  - **Alias** — necesitas una identidad pública derivada de un secreto (función unidireccional)
  - **Prueba** — necesitas demostrar que controlas el alias sin revelar el secreto (firma digital)
- P = d x G es la función unidireccional. Fácil hacia adelante, imposible hacia atrás.
- P2PKH: fondos bloqueados al hash de la clave pública. Solo revelas P al gastar.
- Taproot (P2TR): bloquea directamente a la pubkey, usa Schnorr en vez de ECDSA.

**Frase clave:** "Los mismos dos problemas, en cada tipo de script. Alias + Prueba."

- ¿Por qué ECC sobre RSA? Muestra la tabla: ECC de 256 bits = RSA de 3072 bits. 12x más pequeña.
- Koblitz y Miller (1985): "mismo truco de logaritmo discreto, grupo más difícil"

**Transición:** "Para construir esto, necesitamos matemáticas específicas. Veamos qué reglas gobiernan este mundo."

---

## 01-algebraic-foundations.ipynb (~20 min)

**Este es el módulo más largo. No apures los axiomas — dan frutos en el Módulo 5.**

- Inicio: "Necesitamos una función unidireccional. Pero la operación no puede ser cualquier cosa."
- La operación necesita 5 propiedades. Eso se llama un grupo Abeliano.

**Ejecuta celdas en vivo para cada axioma — usa números pequeños (mod 7):**

| Axioma | Di esto | Celda |
|--------|---------|-------|
| Cerradura | "5+5=10, pero 10 no es impar. La cerradura falló. Por eso usamos un cuerpo finito — mod p nos mantiene dentro." | Celda 2-3 |
| Asociatividad | "El agrupamiento no importa. Aburrido pero esencial — la verificación ECDSA reordena términos." | Celda 4-5 |
| Identidad | "Sumar cero no cambia nada. En la curva, es el punto en el infinito." | Celda 6-7 |
| Inverso | "Cada elemento tiene un compañero que lo deshace. Así es como el verificador revierte el trabajo del firmante." | Celda 8-9 |
| Conmutatividad | "El orden no importa. El firmante y el verificador calculan lo mismo de diferentes maneras." | Celda 10-11 |

- Después de las 5: muestra la tabla de la ecuación ECDSA (celda 12) — "mira, cada propiedad se usa"

**Contexto histórico (intro celda 1):**
- ElGamal: las propiedades de grupo eran GRATIS (enteros mod p, libros de texto desde 1800)
- ECC: mismo esquema, NUEVO grupo — ahora las propiedades son una LISTA DE VERIFICACIÓN
- "No inventaron grupos para ECC. Fueron de compras buscando un grupo más difícil."

**Sección de cuerpos — ve rápido, solo la intuición:**
- "El cuerpo es el terreno donde se dibuja la curva"
- La ecuación de la curva necesita +, -, x → eso es un anillo (celda 13)
- La fórmula de pendiente necesita división → eso es un cuerpo (celda 13)
- Cuerpo finito F_p: mod p lo hace finito y seguro (celda 14-16)
- Ejecuta la tabla de inversos de F_11 (celda 14) — "cada elemento no nulo tiene un inverso"

**Espacio proyectivo — opcional, se puede saltar si hay poco tiempo:**
- Solo se necesita para explicar el punto en el infinito
- "¿Qué pasa cuando sumas un punto a su propio negativo? Línea vertical, sin tercera intersección."
- Espacio proyectivo: las líneas paralelas se encuentran en el infinito. Problema resuelto.
- Si hay tiempo: muestra la esfera plotly (celdas 21-23) — arrastrar para rotar, buen visual

**Transición:** "Ahora conocemos las reglas. Veamos la curva real."

---

## 02-elliptic-curves.ipynb (~8 min)

- Ecuación de Weierstrass: y^2 = x^3 + ax + b
- Bitcoin usa secp256k1: a=0, b=7, entonces y^2 = x^3 + 7
- Ejecuta celda 1: imprime todos los parámetros secp256k1 (P, N, coordenadas de G)
- "P es el primo del cuerpo (donde viven las coordenadas), N es el orden del grupo (donde viven los escalares)"
- Sobre los reales: curva suave. Sobre F_p: puntos dispersos con simetría vertical.
- Ejecuta celda 3: grafica y^2 = x^3 + x + 1 sobre F_23 — "¿ves la simetría?"
- Señala: para cada (x, y) hay (x, p-y)
- No singular: discriminante != 0, sin cúspides ni autointersecciones

**Frase clave:** "La curva es solo un conjunto de puntos. La magia está en lo que hacemos con ellos."

**Transición:** "Tenemos puntos. Ahora sumémoslos."

---

## 03-point-operations.ipynb (~12 min)

**Este es el módulo práctico. Ejecuta cada celda.**

- Ejecuta la celda de preámbulo primero (celda 0) — carga parámetros secp256k1
- Celda 1: clase Point, mod_inverse, point_add, point_double, point_negate
  - "Traza una línea por dos puntos, encuentra el tercero, refleja. Eso es suma."
  - "Línea tangente en un punto: eso es duplicación."
- Celda 2: prueba point_add y point_double con secp256k1 G
  - Muestra: G + G = 2G, y que el resultado está en la curva

**Multiplicación escalar (celda 3-4):**
- "Clave privada d, generador G, clave pública P = d x G"
- Doblar y sumar: O(log k) — "256 duplicaciones y sumas, no 2^256 sumas"
- Ejecuta la demo: elige clave privada aleatoria, calcula clave pública
- "Esta es la función unidireccional. Acabamos de hacerla."

**Claves públicas comprimidas (celda 5-6):**
- 65 bytes sin comprimir (04 || x || y) vs 33 bytes comprimida (02/03 || x)
- "y^2 = x^3+7 tiene dos soluciones para y. Par o impar. Un bit es suficiente."
- Ejecuta: genera clave, serializa comprimida, lee de vuelta, verifica coincidencia

**Transición:** "Podemos hacer claves. Antes de las firmas, veamos de dónde vino esta idea."

---

## 04-key-exchange.ipynb (~8 min)

- ElGamal vs ECC lado a lado (celda 1)
  - "Misma estructura: escalar privado, punto público, secreto compartido"
  - ECDH: Alice tiene (a, A=aG), Bob tiene (b, B=bG), compartido = a*B = b*A = abG
  - Ejecútalo: dos partes, mismo secreto compartido

- Cifrado ECC en curva pequeña (celda 2): y^2 = x^3 - x + 4 sobre F_457
  - Cifra un mensaje como punto de curva
  - "Esto es literalmente ElGamal trasplantado a una curva elíptica"
  - Descifrar: C2 - d*C1 = Pm + k*Q - d*(k*G) = Pm (las k se cancelan)

**Frase clave:** "ECC no es una idea nueva. Es una idea vieja en un grupo más difícil."

**Transición:** "Ahora el evento principal: firmas digitales."

---

## 05-ecdsa.ipynb (~15 min)

**La recompensa. Todo converge aquí.**

- Ejecuta celda de preámbulo primero (celda 0)
- "La función unidireccional se dispara DOS VECES en cada transacción de Bitcoin"
  - Una vez para el alias: P = d x G (tu clave pública)
  - Una vez por firma: R = k x G (punto nonce fresco)

**Firma (celda 1):**
- Recorre la ecuación: s = k^{-1}(z + r*d) mod N
- z = hash del mensaje, r = coordenada x de R, d = clave privada, k = nonce
- Ejecuta: firma un mensaje, imprime (r, s)

**Verificación (celda 2):**
- "El verificador no conoce k ni d. Solo (r, s), z, y P."
- u1 = z/s, u2 = r/s, R' = u1*G + u2*P
- Verifica R'_x == r — "cada propiedad de grupo se usa en este reordenamiento"
- Ejecuta: verify retorna True

**Catástrofe del nonce (celda 3):**
- "Reutiliza k y filtras d. Esto realmente ocurrió — PlayStation 3, 2010."
- Mismo k para dos mensajes → dos ecuaciones, dos incógnitas → resuelve para d
- Ejecuta la demo: dos firmas con mismo k → clave privada extraída
- "Por eso existe RFC 6979 — nonce determinístico a partir de mensaje + clave"

**De matemáticas a bytes (celdas 4-5):**
- Codificación DER: longitud variable, ~72 bytes, formato ASN.1
- Normalización Low-S: s > N/2 → reemplazar con N-s (BIP 62, anti-maleabilidad)
- Schnorr: 64 bytes fijos. Sin DER, sin ambigüedad.
- Muestra el diagrama de diseño de transacción
- Ejecuta celda 5: construye codificación DER desde cero, compara con Schnorr

**Frase clave:** "Las matemáticas producen enteros grandes. DER los envuelve para el cable."

**Transición:** "ECDSA funciona. Pero Bitcoin pasó a algo más limpio."

---

## 06-bitcoin-applications.ipynb (~10 min)

**Schnorr (celda 1-2):**
- "BIP 340. Más simple que ECDSA: s = k + e*d, verificar: sG = R + eP"
- Firma fija de 64 bytes (R_x || s), sin necesidad de codificación DER
- Ventaja clave: **lineal** — las firmas se pueden agregar (MuSig2)
- Ejecuta: firma y verifica con Schnorr
- "Esto es lo que usa Taproot. Cada gasto key-path es una firma Schnorr."

**ECDH en enrutamiento cebolla Lightning (celda 3-4):**
- Enrutamiento cebolla: el remitente envuelve el pago en capas, cada salto pela una
- ECDH en cada salto: secreto compartido desde clave efímera + clave pública del salto
- "Mismo ECDH del Módulo 4, pero ahora cada salto ciega la clave efímera"
- Ejecuta: ruta cebolla de 3 saltos, muestra que cada salto deriva el mismo secreto compartido

**Transición:** "Ese es el panorama completo. Pongamos a prueba tu comprensión."

---

## 07-exercises.ipynb (~15 min o tarea)

**Se puede asignar como tarea o hacer en vivo si hay tiempo.**

- 6 ejercicios, dificultad progresiva:
  1. Aritmética de cuerpos finitos (inverso modular)
  2. Puntos en una curva (encontrar y dado x)
  3. Negación de punto
  4. Traza de doblar y sumar (contar operaciones para un k dado)
  5. Verificar ECDSA a mano (recorrer u1, u2, R')
  6. Recuperación de nonce (extraer clave privada de nonce reutilizado)

- Mapa de conocimiento (celda 8): lista de verificación de todos los conceptos — buena autoevaluación
- Lecturas adicionales (celda 9): enlaces a SEC 2, BIP 340, Silverman, Paar/Pelzl

**Si falta tiempo:** asigna ejercicios 1-4 como tarea, haz 5-6 en vivo (son los de mayor impacto).

---

## Cuadernos Apéndice

Disponibles si surgen preguntas o como material extra:

| Cuaderno | Cuándo usar |
|----------|------------|
| A1-wright-trick.ipynb | "¿Cómo falsificó Craig Wright una firma?" — bueno después del Módulo 5 |
| A2-nonsense-signature.ipynb | "¿Se puede hacer una firma válida sin conocer la clave?" — bueno después de la sección de nonce |
| A3-original-paper.ipynb | Referencia: el artículo de investigación original como cuaderno |

---

## Resumen de Tiempos

| Módulo | Cuaderno | Estimación |
|--------|----------|------------|
| Introducción | 00-intro | 5 min |
| Fundamentos Algebraicos | 01-algebraic-foundations | 20 min |
| Curvas Elípticas | 02-elliptic-curves | 8 min |
| Operaciones de Puntos | 03-point-operations | 12 min |
| Intercambio de Claves | 04-key-exchange | 8 min |
| ECDSA | 05-ecdsa | 15 min |
| Aplicaciones Bitcoin | 06-bitcoin-applications | 10 min |
| Ejercicios | 07-exercises | 15 min |
| **Total** | | **~93 min** |

Si necesitas reducir a 60 min: salta el espacio proyectivo en el Módulo 1, ve rápido por el Módulo 4, asigna ejercicios como tarea.
