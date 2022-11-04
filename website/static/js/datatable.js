$(document).ready(
    function init_datatables(){
        if(typeof($.fn.datatable) === 'undifined'){
            return ;
        }
    $('#datatable_accounts').DataTable();
    $('#datatable_transactions').DataTable();
    $('#datatable_balance').DataTable();
    $('#datatable_account_details').DataTable();
});