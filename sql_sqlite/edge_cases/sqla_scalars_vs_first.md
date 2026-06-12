# SQLA scalars, scalar_one, first ()
## STMT
 stmt = select(models.AgreementSigner).where(
                models.AgreementSigner.agreement_id == agrmnt_pkid,
                models.AgreementSigner.signer_email == "ernesto@email.com",
            )

            # --- Edge case testing
            # signer_record_list = session.execute(
            #     stmt
            # ).all()  # lista de objetos AgreementSigner
            # content= [(AgreementSigner(email='leon@email.com', full_name='Leonardo', role='APPROVER', label= None),), (AgreementSigner(email='leon@email.com', full_name='Leonardo', role='APPROVER', label= None),)]

            signer_record_scalar = session.execute(
                stmt
            ).scalar_one_or_none()  # instancia de Agreement Signer
            # content= AgreementSigner(email='ernesto@email.com', full_name='Ernesto', role='APPROVER', label= None)
            logger.debug(
                f" signer_record_scalar type:{type(signer_record_scalar)}\n content= {signer_record_scalar} "
            )

            signer_record_first = session.execute(
                stmt
            ).first()  # item SQLA.row
            # content= (AgreementSigner(email='ernesto@email.com', full_name='Ernesto', role='APPROVER', label= None),)
            logger.debug(
                f" signer_record_first type:{type(signer_record_first)}\n content= {signer_record_first} "
            )
