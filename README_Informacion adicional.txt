Template: list.html
    * object_list es el listado de objetos
    title       titulo de la hoja
    busqueda    habilita el cuadro de busqueda
        buscar      texto del boton buscar
        limpiar     texto del boton limpiar
    create 
        url         url del formulario
        display     valor que se muestra si no hay imagen y tooltip
        img         nombre de la imagen (con su extesión)
    campos
        enumerar    -1: no enumero, 0: enumera base 0, 1: enumero base 1 (hace uso de la paginación)
        lista       campos del objeto que se debem desplegar en la tabla
        opciones    titulo a desplegar de las opciones, si no hay valor no las muestra
    campos_extra (antes campos_adicionales)
        nombre  display del campo adicional que se mostrará
        __ debe tener uno de estos valores __
        valor       se evalúa en primer lugar y se muestra si lo tiene (con un formato definido)
        funcion     se evalúa en segundo y ejecuta la funcion mostrando el valor devuelto
        ul_lista    se evalúa y se muestra la lista correspondiente
        url         envía un enlace
        target      (propio de url) para determinar donde se abre el enlace
        img         (proio de url) para el boton
        constante   se evalúa como default y se muestra (sin formato)
    opciones
        detail      display para la opcion ver detalle del objeto
        detail_img  imagen de la opcion ver detalle del objeto (con extensión)
        update      display para la opcion actualizar del objeto
        update_img  imagen de la opcion actualizar del objeto (con extensión)
        delete      display para la opcion eliminar del objeto
        delete_img  imagen de la opcion eliminar del objeto (con extensión)
    mensaje
        vacio   mensaje cuando no se encuentren objetos
    permisos
        create      define el permiso para el boton nuevo/agregar
        update      define el permiso para el boton actualizar (opciones)
        delete      define el permiso para el boton eliminar (opciones)
    botones_extra
        permiso     permiso para la acción del boton
        url         url de la acción
        display     valor que se muestra si no hay imagen y tooltip
        img         nombre de la imagen (con su extesión)
        target      (opcional) si no hay target se refresca en la misma ventana
Template: forms.html
    * object es el objeto que se modifica
    title       titulo de la hoja
    busqueda    habilita el cuadro de busqueda
        buscar      texto del boton buscar
        limpiar     texto del boton limpiar
    object      mensaje o información que se dese mostrar en el formulario
    form        formulario pricipal
    aditional_form formulario adicional si hubiera (formularios compuestos)
Template: detail.html
    * object es el objeto que se muestra
    title       titulo de la hoja
    busqueda    habilita el cuadro de busqueda
        buscar      texto del boton buscar
        limpiar     texto del boton limpiar
    campos
        lista   listado de campos que se desea mostrar de forma individual en la vista
        opciones    titulo a desplegar de las opciones, si no hay valor no las muestra
    campos_extra (arreglo)
        nombre  display del campo adicional que se mostrará
        __ debe tener uno de estos valores __
        valor       se evalúa en primer lugar y se muestra si lo tiene (con un formato definido)
        funcion     se evalúa en segundo y ejecuta la funcion mostrando el valor devuelto
        ul_lista    se evalúa y se muestra la lista correspondiente
        porcentaje  para falores flotantes desplegados con formato %
        url         envía un enlace
        target      (propio de url) para determinar donde se abre el enlace
        img         (proio de url) para el boton
        constante   se evalúa como default y se muestra (sin formato)
    opciones
        update      display para la opcion actualizar del objeto
        update_img  imagen de la opcion actualizar del objeto (con extensión)
        delete      display para la opcion eliminar del objeto
        delete_img  imagen de la opcion eliminar del objeto (con extensión)
    permisos
        update      define el permiso para el boton actualizar (opciones)
        delete      define el permiso para el boton eliminar (opciones)
    botones_extra
        permiso     permiso para la acción del boton
        url         url de la acción
        display     valor que se muestra si no hay imagen y tooltip
        img         nombre de la imagen (con su extesión)
        target      (opcional) si no hay target se refresca en la misma ventana
    forms <formularios modal para superponerlo en la pagina>
        modal       nombre para identificar el formulario modal para mostrar en la misma pantalla (debe ser único)
        display     tooltip y nombre en caso de no poder mostrar la imagen
        link_img    imagen del boton
        action      url que recibe la acción del formulario
        form        formulario
        opciones    
            submit  texto que mostrará el boton enviar del formulario
    tables          (subsección agregada al detail)
        title       titulo de la sección ocupada por la tabla
        object_list
        enumerar    enumerar    -1: no enumero, 0: enumera base 0, 1: enumero base 1 (hace uso de la paginación)
        lista       campos del objeto que se debem desplegar en la tabla
        campos_extra
            nombre  display del campo adicional que se mostrará
            __ debe tener uno de estos valores __
            valor       se evalúa en primer lugar y se muestra si lo tiene (con un formato definido)
            funcion     se evalúa en segundo y ejecuta la funcion mostrando el valor devuelto
            ul_lista    se evalúa y se muestra la lista correspondiente
            constante   se evalúa como default y se muestra (sin formato)
        opciones    titulo a desplegar de las opciones, si no hay valor no las muestra
            <imagenes y display utiliza las mismas que en la sección pricipal del detail>
        permisos
            detail_img <si existe utiliza este icono en el boton, si no utiliza el generico de la pantalla>
            update      define el permiso para el boton actualizar (opciones)
            update_img  <si existe utiliza este icono en el boton, si no utiliza el generico de la pantalla>
            update_display  <display o tooltip que se desea en el icono del modal>
            update_modal    <si se desea que se desplique el formulario en el modal indicado>    
            delete  define el permiso para el boton eliminar (opciones)
            delete_img <si existe utiliza este icono en el boton, si no utiliza el generico de la pantalla>
            delete_display  <display o tooltip que se desea en el icono del modal>
            delete_modal    <si se desea que se desplique el formulario en el modal indicado>    
        next        se utiliza para definir un redireccionamiento posterior a enviar el formulario
 ***manual_tables   (subsección agregada al detail)
Template: delete_confirmation.html
    * object es el objeto que se muestra
    title       titulo de la hoja
    busqueda    habilita el cuadro de busqueda
        buscar      texto del boton buscar
        limpiar     texto del boton limpiar
    form        formulario de eliminación
    opciones
        confirmación    mensaje de confirmación
        submit          texto que se mostrará en el boton enviar del formulario
Template: templatedetail_multiple_objects.html
    title       titulo de la hoja
    busqueda    habilita el cuadro de busqueda
        buscar      texto del boton buscar
        limpiar     texto del boton limpiar
    objects         (arreglo)
        object      objeto con la información a mostrar
        campos
            lista   listado de campos que se desea mostrar de forma individual en la vista
        campos_extra (arreglo)
            nombre  display del campo adicional que se mostrará
            __ debe tener uno de estos valores __
            valor       se evalúa en primer lugar y se muestra si lo tiene (con un formato definido)
            funcion     se evalúa en segundo y ejecuta la funcion mostrando el valor devuelto
            ul_lista    se evalúa y se muestra la lista correspondiente
            url         envía un enlace
            target      (propio de url) para determinar donde se abre el enlace
            img         (proio de url) para el boton
            constante   se evalúa como default y se muestra (sin formato)
    opciones
        display     titulo a desplegar de las opciones, si no hay valor no las muestra
        update      display para la opcion actualizar del objeto
        update_img  imagen de la opcion actualizar del objeto (con extensión)
        update_perm define el permiso para el boton actualizar (opciones)
        delete      display para la opcion eliminar del objeto
        delete_img  imagen de la opcion eliminar del objeto (con extensión)
        delete_perm define el permiso para el boton eliminar (opciones)
    botones_extra
        permiso     permiso para la acción del boton
        url         url de la acción
        display     valor que se muestra si no hay imagen y tooltip
        img         nombre de la imagen (con su extesión)
        target      (opcional) si no hay target se refresca en la misma ventana
    forms <formularios modal para superponerlo en la pagina>
        modal       nombre para identificar el formulario modal para mostrar en la misma pantalla (debe ser único)
        display     tooltip y nombre en caso de no poder mostrar la imagen
        link_img    imagen del boton
        action      url que recibe la acción del formulario
        form        formulario
        opciones    
            submit  texto que mostrará el boton enviar del formulario
    tables          (subsección agregada al detail)
        title       titulo de la sección ocupada por la tabla
        object_list
        enumerar    enumerar    -1: no enumero, 0: enumera base 0, 1: enumero base 1 (hace uso de la paginación)
        lista       campos del objeto que se debem desplegar en la tabla
        campos_extra
            nombre  display del campo adicional que se mostrará
            __ debe tener uno de estos valores __
            valor       se evalúa en primer lugar y se muestra si lo tiene (con un formato definido)
            funcion     se evalúa en segundo y ejecuta la funcion mostrando el valor devuelto
            ul_lista    se evalúa y se muestra la lista correspondiente
            constante   se evalúa como default y se muestra (sin formato)
        opciones    titulo a desplegar de las opciones, si no hay valor no las muestra
            <imagenes y display utiliza las mismas que en la sección pricipal del detail>
        permisos
            update  define el permiso para el boton actualizar (opciones)
            delete  define el permiso para el boton eliminar (opciones)
        next        se utiliza para definir un redireccionamiento posterior a enviar el formulario
 ***manual_tables   (subsección agregada al detail)
