import PropTypes from "prop-types";
import { useState } from "react";
import { observer } from "mobx-react-lite";
import SimpleButton from "../Buttons/SimpleButton";
import EditButton from "../Buttons/EditButton";
import TelegramScraperEditForm from "../Forms/TelegramScraper/TelegramScraperEditForm";
import TelegramScraperDeleteForm from "../Forms/TelegramScraper/TelegramScraperDeleteForm";
import TelegramScraperToggleRunningStatusForm from "../Forms/TelegramScraper/TelegramScraperToggleRunningStatusForm";

const TableItem = observer(
    ({ id, name, total, totalPerMonth, totalPerDay, origin, isRunning }) => {
        const [editFormIsDisable, setEditFormIsDisable] = useState(true);
        const [deleteFormIsDisable, setDeleteFormIsDisable] = useState(true);
        const [
            toggleRunningStatusFormIsDisable,
            setToggleRunningStatusFormIsDisable,
        ] = useState(true);

        return (
            <>
                <TelegramScraperEditForm
                    disable={editFormIsDisable}
                    disableSetter={setEditFormIsDisable}
                    telegramScraperId={id}
                />
                <TelegramScraperDeleteForm
                    disable={deleteFormIsDisable}
                    disableSetter={setDeleteFormIsDisable}
                    telegramScraperId={id}
                />
                <TelegramScraperToggleRunningStatusForm
                    disable={toggleRunningStatusFormIsDisable}
                    disableSetter={setToggleRunningStatusFormIsDisable}
                    telegramScraperId={id}
                />
                <div className='h-[184px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-roboto'>
                    <div className='h-[56px] w-[10vw] flex items-center font-medium text-[1.1vw]'>
                        <span className='truncate'>{name}</span>
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
                        <a href={origin} className='truncate'>
                            <span className='underline'>{origin}</span>
                        </a>
                    </div>
                    <div className='w-[10vw] flex flex-col gap-[10px]'>
                        {isRunning ? (
                            <SimpleButton
                                handleClick={() =>
                                    setToggleRunningStatusFormIsDisable(false)
                                }
                                filled={true}
                            >
                                Остановить
                            </SimpleButton>
                        ) : (
                            <SimpleButton
                                handleClick={() =>
                                    setToggleRunningStatusFormIsDisable(false)
                                }
                            >
                                Запустить
                            </SimpleButton>
                        )}
                        <div className='flex justify-between'>
                            <EditButton
                                handleClick={() => setEditFormIsDisable(false)}
                            />
                            <span
                                onClick={() => setDeleteFormIsDisable(false)}
                                className='font-medium underline flex items-center hover:cursor-pointer'
                            >
                                Удалить
                            </span>
                        </div>
                    </div>
                </div>
            </>
        );
    }
);

TableItem.propTypes = {
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    total: PropTypes.number.isRequired,
    totalPerMonth: PropTypes.number.isRequired,
    totalPerDay: PropTypes.number.isRequired,
    origin: PropTypes.string.isRequired,
    isRunning: PropTypes.bool.isRequired,
};

export default TableItem;
