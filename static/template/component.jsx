import React from 'react';
import PropTypes from 'prop-types';

export const %%NAAM%% = ({label, image, ...props }) => {
    return (
        <div>
            <b>{label}</b>
            <div dangerouslySetInnerHTML={{__html: image}}/>
        </div>

    )
}
