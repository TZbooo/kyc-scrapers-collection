import PropTypes from "prop-types";
import CancelIcon from "../../assets/cancel.svg";

const CancelFormButton = ({ handleClick }) => {
    return (
        <>
            <div
                onClick={handleClick}
                className='rounded-[3px] border-[#2E2E2E] border-[1px] p-[21px] self-end hover:cursor-pointer'
            >
                <img src={CancelIcon} />
            </div>
        </>
    );
};

CancelFormButton.propTypes = {
    handleClick: PropTypes.func.isRequired,
};

export default CancelFormButton;
