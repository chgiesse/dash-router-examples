from flash import clientside_callback, Input
from dash_router import RootContainer


clientside_callback(
    '''
    //js
    function(url) {
        if (typeof url !== 'string') { return; }
        
        const progressBar = document.querySelector('#nprogress .bar');
        if (!progressBar) { return; }
        
        if (url.includes('nested-route')) {
            progressBar.style.display = 'none';
        } else {
            progressBar.style.display = 'block'; // or '' to restore default
        }
    }
    ;//
    ''',
    Input(RootContainer.ids.location, 'pathname')
)