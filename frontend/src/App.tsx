import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "./App.css";
import folderIcon from "./assets/folder-icon.svg";
import { SummaryResponse } from "./interfaces/SummaryResponse";
import SummaryTable from "./components/Table";

function App() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [response, setResponse] = useState<SummaryResponse | null>(null);

    const [isUploading, setIsUploading] = useState(false);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleUpload = async (event: React.FormEvent) => {
        event.preventDefault();

        if (!selectedFile) return;

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            setIsUploading(true);
            const res = await fetch(
                "https://nlp-resume-parser-bxyn.onrender.com/upload",
                {
                    method: "POST",
                    body: formData,
                }
            );

            const data = await res.json();
            if (res.ok) {
                setResponse(data);
            } else {
                toast.error("Unexpected error occurred.");
            }
        } catch (error) {
            toast.error("Unexpected error occurred.");
        } finally {
            setIsUploading(false);
        }
    };

    const resetForm = () => {
        setSelectedFile(null);
        setResponse(null);
    };

    return (
        <>
            {response ? (
                <div className="max-w-4xl flex flex-col items-center text-center bg-white rounded-lg p-10">
                    <SummaryTable response={response} />
                    <button
                        onClick={resetForm}
                        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                        Upload Another
                    </button>
                </div>
            ) : (
                <div className="flex flex-col items-center justify-center gap-10 w-[400px] min-h-[500px] bg-white rounded-[40px] shadow-2xl">
                    <div className="flex flex-col justify-center items-center">
                        <h1 className="text-4xl font-normal">
                            Upload a resume
                        </h1>
                        <p className="text-lg font-medium text-gray-600">
                            PDF, DOCX
                        </p>
                    </div>

                    <form
                        onSubmit={handleUpload}
                        className="flex flex-col items-center justify-center w-3/4 h-48 border-gray-800 border-[1px] border-dashed rounded-[20px]">
                        <label
                            htmlFor="file-upload"
                            className="hover:cursor-pointer hover:scale-105 duration-300 flex flex-col items-center justify-center bg-orange-500 bg-opacity-10 w-28 h-28 rounded-full">
                            <img src={folderIcon} alt="Open Folder Image" />
                            <input
                                type="file"
                                className="hidden"
                                id="file-upload"
                                onChange={handleFileChange}
                            />
                        </label>
                        {selectedFile && (
                            <button
                                disabled={isUploading}
                                type="submit"
                                className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                                {isUploading ? "Processing" : "Proceed"}
                            </button>
                        )}
                    </form>
                </div>
            )}
            <ToastContainer />
        </>
    );
}

export default App;
