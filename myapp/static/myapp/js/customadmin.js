
$(document).ready(function() {
    let subCourseFormIndex = $('#sub-course-forms').children().length;
    
    $('#add-sub-course').click(function() {
        const newForm = $('#sub-course-forms').children().first().clone(true);
        newForm.find('input').each(function() {
            const name = $(this).attr('name').replace('-0-', `-${subCourseFormIndex}-`);
            const id = $(this).attr('id').replace('-0-', `-${subCourseFormIndex}-`);
            $(this).attr({ 'name': name, 'id': id }).val('');
        });
        newForm.find('textarea').each(function() {
            const name = $(this).attr('name').replace('-0-', `-${subCourseFormIndex}-`);
            const id = $(this).attr('id').replace('-0-', `-${subCourseFormIndex}-`);
            $(this).attr({ 'name': name, 'id': id }).val('');
        });
        $('#sub-course-forms').append(newForm);
        subCourseFormIndex++;
    });

    $('.remove-sub-course').click(function() {
        $(this).closest('.sub-course-form').remove();
    });
});


