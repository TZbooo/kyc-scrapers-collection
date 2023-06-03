import PropTypes from "prop-types";
import CheckIcon from "../../assets/check.svg";

const Checkbox = ({ checked, checkedSetter, placeholder }) => {
    return (
        <>
            <div onClick={() => checkedSetter(!checked)} className='flex gap-[20px] items-center'>
                {checked ? (
                    <div className='bg-[#F0F0F0] border-[#989898] border-[1px] h-[20px] w-[20px] rounded-[3px] ml-[3px]'>
                        <img src={CheckIcon} />
                    </div>
                ) : (
                    <div className='bg-[#F0F0F0] border-[#989898] border-[1px] h-[20px] w-[20px] rounded-[3px] ml-[3px]'></div>
                )}
                <span className='text-[#C9C9C9]] font-roboto'>
                    {placeholder}
                </span>
            </div>
        </>
    );
};

Checkbox.defaultProps = {
    checked: false,
};

Checkbox.propTypes = {
    checked: PropTypes.bool.isRequired,
    checkedSetter: PropTypes.func.isRequired,
    placeholder: PropTypes.string.isRequired,
};

export default Checkbox;
