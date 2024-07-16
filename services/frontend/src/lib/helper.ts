const capitalizeAndRemoveUnderscore = (str: string) => {
    return str
        .split('_')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};

const getFormatFile = (videoUrl: string) => {
    return videoUrl.split('.').pop()?.toLowerCase() || '';
};

export { capitalizeAndRemoveUnderscore, getFormatFile };
