import PropTypes from "prop-types";

const TableHeaders = ({ headers }) => {
    return (
        <>
            <div className='h-[116px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-semibold font-roboto text-[1.3vw] leading-[28.13px]'>
                {headers.map((header) => (
                    <div
                        key={header.id}
                        className='h-[56px] w-[10vw] flex items-center'
                    >
                        {header.name}
                    </div>
                ))}
            </div>
        </>
    );
};

TableHeaders.propTypes = {
    headers: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
    })).isRequired,
};

export default TableHeaders;
