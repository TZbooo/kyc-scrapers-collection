import PropTypes from "prop-types";
import EditIcon from "../../assets/edit.svg";
import SimpleButton from "../Buttons/SimpleButton";

const TableItem = ({
    name,
    total,
    totalPerMonth,
    totalPerDay,
    origin,
    isRunning,
}) => {
    return (
        <>
            <div className='h-[184px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-roboto'>
                <div className='h-[56px] flex items-center font-medium text-[1.1vw]'>
                    {name}
                </div>
                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                    {total}
                </div>
                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                    {totalPerMonth}
                </div>
                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                    {totalPerDay}
                </div>
                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                    {origin}
                </div>
                <div className='w-[10vw] flex flex-col gap-[10px]'>
                    {isRunning ? (
                        <SimpleButton filled={true}>Остановить</SimpleButton>
                    ) : (
                        <SimpleButton>Запустить</SimpleButton>
                    )}
                    <div className='flex justify-between'>
                        <div className='rounded-[3px] border-[#212121] border-[1px] py-[10px] pl-[12px] pr-[11px]'>
                            <img src={EditIcon} />
                        </div>
                        <span className='font-medium underline flex items-center'>
                            Удалить
                        </span>
                    </div>
                </div>
            </div>
        </>
    );
};

TableItem.propTypes = {
    name: PropTypes.string.isRequired,
    total: PropTypes.number.isRequired,
    totalPerMonth: PropTypes.number.isRequired,
    totalPerDay: PropTypes.number.isRequired,
    origin: PropTypes.string.isRequired,
    isRunning: PropTypes.bool.isRequired,
};

export default TableItem;
