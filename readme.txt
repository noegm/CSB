CDR BUILDER


Uso

SENCILLO

python3 CDR_builder.py <confFile> <cdrTemplate>

El confFile contiene los datos de fechas del CONSUMO, las OB implicadas, tanto en la 
generación de los CDRs como en la que está el cliente, y las subscripciones implicadas

Si hay más de 1 subscripción, el fichero final contendrá tantas réplicas los datos del 
fichero de entrada como subscripciones haya

El template del cdr difiere del real en que no tiene ni línea de cabecera ni de pie, 
dichas líneas las añade este generador

Los campos del CDR están todos parametrizados menos el tipo de línea ("línea de datos" 
indicado con valor hardcoded '20'), el resource_id (que ha de rellenarse de forma manual) 
y los códigos y cantidades del uso propiamente

El resource_id se deja "manual" para poder identificar físicamente el mismo recurso a lo 
largo de todos los días (un fichero por día)

Si hay solamente 1 subscripción se puede configurar el template previamente al generador, 
pero si hay más de una subscripción, al ser replicado dicho template, el resource_id 
también se replicaría y sería incorrecto formalmente, aunque en estos momentos no afecta
al servicio de Billing

Plantillas actuales que usan este script:
cdr.template
cdr_Acens.template
cdr_EFT-GLB-006.template
cdr_EFT-GLB-009.template


CONSUMOS PASADOS

python3 CDR30_builder.py <confFile> <cdrTemplate>

A diferencia de la anterior, esta versión se puede usar para generar CDRs que simulan registros
con consumos de 2 días antes respecto a la fecha de generación, en lugar del consumo esperado del
día anterior. Son los registros con el primer campo con valor 30

Aplican todas las limitaciones de la versión anterior



CONTROL DE RESOURCE_ID

python3 CDR30_builder_w-rsrcId.py <confFile> <cdr_w-rsrcId_Template>

Esta versión, además de incorporar la gestión de los registros "30" de consumo pasado,
permite la gestión de los resource-Id.

Con el identificador adecuado en el template el generador gestionará un resourceId diferente para 
cada identificador por cada subscripción y lo repetirá correctamente para cada una todos los días, 
tanto en los registros de consumo normal (tipo 20) como de consumo pasado (tipo 30).
Para ello hay que editar el template y ponerle un "tag" distinto a cada recurso distinto, es decir,
si 2 líneas comparten el mismo tag, el resourceId será el mismo. Este uso es requerido para el caso
de tener registros 30 (uso retrasado) y 20 (uso estándar) del mismo recurso en el mismo fichero

Hay que tener en cuenta que la phaseII-0 de VIVO usará discriminación por resource_id, así que la 
última frase del uso SENCILLO no aplicaría y es obligatoria la gestión correcta, no solamente 
formal, del resource_id


Plantillas actuales que usan este script:
cdr_w-rsrcId.template
