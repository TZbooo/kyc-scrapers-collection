import PropTypes from "prop-types";

const SimpleButton = ({ children, filled }) => {
    return (
        <>
            {filled ? (
                <button className='bg-[#212121] text-white font-semibold rounded-[3px] py-[12px] px-[30px] flex gap-[11px] items-center justify-center'>
                    {children}
                </button>
            ) : (
                <button className='font-semibold rounded-[3px] border-[#212121] border-[1px] py-[12px] px-[30px]'>
                    {children}
                </button>
            )}
        </>
    );
};

SimpleButton.defaultProps = {
    filled: false,
};

SimpleButton.propTypes = {
    children: PropTypes.element.isRequired,
    filled: PropTypes.bool,
};

export default SimpleButton;
