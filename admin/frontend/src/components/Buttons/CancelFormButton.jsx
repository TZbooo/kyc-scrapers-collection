import CancelIcon from "../../assets/cancel.svg";

const CancelButton = () => {
    return (
        <>
            <div className='rounded-[3px] border-[#2E2E2E] border-[1px] p-[21px] self-end'>
                <img src={CancelIcon} />
            </div>
        </>
    );
};

export default CancelButton;
