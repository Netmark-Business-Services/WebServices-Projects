def Test2():
    manager = Aliases.HealthEdge_Manager
    home_form = manager.HomeForm
    main_panel = home_form.panelControlDetail
    docked_bar = home_form.BarDockControl.DockedBarControl

    # --- Step 1: Search Supplier by HCC Identifier ---
    provider_widget = main_panel.homeTab1.WidgetsHost.WidgetContainer.ProviderWidgetControl
    provider_widget.xtraScrollableControlProviders.TaskRow.panelControlTop.panelControlTaskLinks.SimpleButtonSearch.ClickButton()

    search_dialog = manager.SearchDialog
    supplier_search_box = search_dialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit
    supplier_search_box.SetText("1004052")
    search_dialog.BarDockControl.DockedBarControl.ClickItem("Search")
    search_dialog.panelControl1.standaloneBarDockControlTasks.DockedBarControl.ClickItem("View")

    # --- Step 2: Navigate to Correspondence Tab ---
    main_panel.SupplierView.xtraTabControlSupplier.ClickTab("Correspondence")

    # --- Step 3: Open Send Correspondence Dialog ---
    docked_bar.ClickItem("Send Correspondence")
    send_dialog = manager.SendCorrespondenceDlg

    # --- Step 4: Select Correspondence Type ---
    correspondence_panel = send_dialog.panelBottom.xtraTabControlEdit.xtraTabPageEdit.CorrespondenceEditControl.xtraScrollableControl1.correspondenceDetails.entityPanelCorrespondence
    correspondence_panel.headerGroupControlCorrespondence.lookupCorrespondence.Click(130, 6)
    manager.PopupLookUpEditForm.Click(115, 26)

    # --- Step 5: Select Payment for Correspondence Subject ---
    payment_subject_panel = correspondence_panel.headerGroupControlCorrespondenceSubject.subEntityPanelCorrespondenceSubject.entityPanelPayment
    payment_subject_panel.Click(292, 11)

    reference_menu_button = payment_subject_panel.referenceMenuButtonPayment
    reference_menu_button.Click(5, 7)
    reference_menu_button.PopupMenu.Click("Look up")

    # --- Step 6: Resolve Payment using Check Number ---
    resolve_dialog = manager.ResolveDialog
    resolve_panel = resolve_dialog.panelControlLeft.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.PaymentSearchCriteria
    check_no_box = resolve_panel.entityPanelPaymentSearchInput.autoEditCheckNo.panelControlAutoEdit.TextEdit
    check_no_box.SetText("6257")

    resolve_dialog.panelControlLeft.panelControlSearch.simpleButtonSearch.ClickButton()
    resolve_dialog.panelControlBottom.simpleButtonOK.ClickButton()

    # --- Step 7: Send Correspondence and Confirm ---
    send_dialog.BarDockControl.DockedBarControl.ClickItem("Send")
    manager.PromptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()

    # --- Step 8: Return to Home ---
    docked_bar.ClickItem("Home")