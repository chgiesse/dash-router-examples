var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.CustomLoadingOverlay = function (props) {
    return React.createElement(
        window.dash_mantine_components.Loader,
        {
            setProps: (props) => {
                return props
            }
        }
    );
};
