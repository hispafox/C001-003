interface Props {
  message: string;
}

/** Mensaje de error reutilizable. */
export default function ErrorMessage({ message }: Props) {
  return <p className="error-message">⚠️ {message}</p>;
}
