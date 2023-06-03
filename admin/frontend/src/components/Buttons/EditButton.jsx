import PropTypes from "prop-types";
import EditIcon from "../../assets/edit.svg";

const EditButton = ({ handleClick }) => {
    return (
        <>
            <div
                onClick={() => handleClick()}
                className='rounded-[3px] border-[#212121] border-[1px] py-[10px] pl-[12px] pr-[11px] hover:cursor-pointer'
            >
                <img src={EditIcon} />
            </div>
        </>
    );
};

EditButton.propTypes = {
    handleClick: PropTypes.func.isRequired,
};

export default EditButton;
