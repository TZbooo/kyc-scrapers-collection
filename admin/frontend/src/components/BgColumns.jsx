import PropTypes from "prop-types";

const BgColumns = ({ columnsCount }) => {
    return (
        <>
            <div className='flex px-[60px] w-[100%] justify-between absolute z-[-1]'>
                {new Array(columnsCount).fill(
                    <div className='w-[1px] h-[100vh] bg-[#f0efef]'></div>
                )}
            </div>
        </>
    );
};

BgColumns.defaultProps = {
    columnsCount: 5,
};

BgColumns.propTypes = {
    columnsCount: PropTypes.number,
};

export default BgColumns;
