CDR BUILDER


Uso 

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



 
