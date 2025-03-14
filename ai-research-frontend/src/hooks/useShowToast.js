import { useCallback } from 'react'
import { toaster } from '../components/ui/toaster'

const useShowToast = () => {
    const showToast = useCallback((title, description, status) => {
        if (toaster && toaster.create) {
            toaster.create({
                title: title,
                description: description,
                status: status,
                duration: 3000,
                action: {
                    label: "Close",
                    onClick: () => console.log("Undo"),
                }
            });
        } else {
            console.error('Toaster object or create method is not available');
        }
    }, []);

    return showToast;
}

export default useShowToast;
